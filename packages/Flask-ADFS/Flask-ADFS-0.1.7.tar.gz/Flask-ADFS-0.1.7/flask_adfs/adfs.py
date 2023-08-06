from flask import Blueprint, jsonify
from flask import current_app as app
from flask_login import login_user, current_user
from flask import render_template,  redirect, request, session, url_for, Blueprint, g, abort

import requests

from flask import current_app as app
from urllib.parse import urlparse

from flask_adfs.model import User
from flask_adfs.decorators import role_required
from .initialise import login_mgr, get_access
from sys import getsizeof

# This is the blueprint object that gets registered into the app in blueprints.py.
adfs_bp = Blueprint('adfs_bp', __name__, template_folder='templates')


# TODO JP need to get template into library
@adfs_bp.route('/adfs/getcookie', methods=['GET'])
@role_required("view")
def xxx():
    goto = request.args.get("redirect", url_for('adfs_bp.guard'))
    return render_template('getcookie.html', redirect=goto)


@adfs_bp.route('/adfs/guard/', methods=['GET'])
@role_required("view")
def guard(index=None):
    # for the moment create a stub until authentication is in place
    # access = {'id':'cs062jp',
    #  'roles':['Administrator','Approver','Author','Editor','Publisher','Reviewer','Viewer']}
    permissions = {}
    for channel, perms in get_access().items():
        cx = permissions.setdefault(channel,{})
        for perm, roles in perms.items():
            cx[perm] = not roles.isdisjoint(current_user.get_roles())

    access = {'id': current_user.get_racf_id(), 'roles': list(current_user.get_roles()), 'permissions': permissions}
    return jsonify(access)


def log_session(label, session):
    app.logger.debug(label + ': session cookie size = {0}'.format(getsizeof(session)))
    for key, val in session.items():
        if key not in ['access_token']:
            app.logger.debug(label + " : session cookie {0}:{1}".format(key, val))
        else:
            app.logger.debug(label + " : session cookie {0}:{1}-{2}".format(key, val[:4],val[-4:]))


@adfs_bp.route('/login', methods=['GET', 'POST'])
def login():  # pragma: no cover
    # log_session('/login',session)

    # prevent redirections to this page
    requested_page = session.get('requested_page', '').strip()
    o = urlparse(requested_page)
    this_url = url_for("adfs_bp.login", _external=False)
    if o.path == this_url:
        abort(403, 'Abort: direct access to login page not allowed' )

    if not requested_page:
        app.logger.error('Abort: No page requested')
        abort(403, 'Invalid page requested {0}'.format(request.url))

    if app.config.get('LOGIN_DISABLED') or current_user.is_authenticated:
        app.logger.error('/login login disabled ({0}) or already authenticated ({1})'.format
                         (app.config.get('LOGIN_DISABLED'), current_user.is_authenticated))  # should never get here
        if 'requested_page' in session:
            del session['requested_page']
        if  'access_token' in session:
            del session['access_token']
        return redirect(requested_page)
    else:
        user_ticket = request.args.get("code")
        if user_ticket is None:
            script_root = request.script_root
            if script_root.startswith('/'):
                script_root = script_root[1:]
            auth_url = (app.config.get('ADFS_URL') + "/adfs/oauth2/authorize?" +
                "response_type=code&client_id=" + app.config.get('ADFS_CLIENT_ID') +
                "&redirect_uri=" + app.config.get('ADFS_LOGIN_URL') +
                "&resource=" + app.config.get('ADFS_LOGIN_URL') +
                "&state=" + script_root)
            return redirect(auth_url)
        else:
            return OAUTH_validate(user_ticket)


ERROR_TEMPLATE='errors/login_error.html'

def OAUTH_validate(user_ticket):  # pragma: no cover
    access_token = validate_user_ticket(user_ticket)
    if access_token in ["","unable to get access token using access ticket"]:
        app.logger.error('OAUTH_validate failed')
        return abort(403) # Forbidden
    user = User(access_token=access_token)
    try:
        if not user.is_authenticated:
            app.logger.error('user not authenticated')
            return render_template(ERROR_TEMPLATE, requested_page=session['requested_page']), 403
        login_user(user)
        session['access_token'] = access_token
        try:
            if session.get('requested_page') is None:
                abort(404) # Not Found
            redirect_uri = session['requested_page']
            del session['requested_page']
            return redirect(redirect_uri)
        except:
            abort(404) # Not Found

    except:
        app.logger.error('exception login_user')
        return render_template(ERROR_TEMPLATE, requested_page=session['requested_page']), 403


def validate_user_ticket(user_ticket):  # pragma: no cover
    request_body = ("grant_type=authorization_code&client_id=" + app.config.get('ADFS_CLIENT_ID') +
                    "&redirect_uri=" + app.config.get('ADFS_LOGIN_URL')
                    + "&code=" + user_ticket)

    url = app.config.get("ADFS_URL") + '/adfs/oauth2/token'

    resp = requests.get(url, data=request_body)
    if resp.status_code == 200:
        try:
            resp = resp.json()
            return resp['access_token']
        except:
            app.logger.error('ADFS Ticket Not Validated')
            pass
    return ''


@login_mgr.user_loader
def load_user(user_id):  # pragma: no cover
    try:
        # log_session('load user',session)

        g.user = User(access_token=session['access_token'])
        return g.user
    except:
        app.logger.error('load user failed')
        return None


@login_mgr.unauthorized_handler
def handle_needs_login():
    # import pudb; pudb.set_trace()

    if 'access_token' in session:
        del session['access_token']
    session['requested_page'] = request.url
    return redirect(url_for("adfs_bp.login", _external=False))
