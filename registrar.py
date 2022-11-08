

import flask
from database import DatabaseQuery

app = flask.Flask(__name__, template_folder='.')

@app.route('/', methods = ['GET'])
@app.route('/course_search', methods = ['GET'])
def course_search():
    dept = flask.request.args.get("dept")
    if dept is None:
        dept = ""
    num = flask.request.args.get("num")
    if num is None:
        num = ""
    area = flask.request.args.get("area")
    if area is None:
        area = ""
    title = flask.request.args.get("title")
    if title is None:
        title = ""

    # if error with database show error page
    success, courses = DatabaseQuery.search_reg(
        dept,
        num,
        area,
        title)
    if success is not True:
        error_msg = "A server error occured. Please contact the "+\
          "system administrator."
        html_code =  flask.render_template("errorpage.html", error_msg \
                                         = error_msg)
        response = flask.make_response(html_code)
        return response

    html_code = flask.render_template("coursesearch.html",
                                      prev_dept = dept,
                                      prev_num = num,
                                      prev_area = area,
                                      prev_title = title,
                                      courses = courses)
    response = flask.make_response(html_code)
    return response

@app.route("/course_details", methods = ['GET'])
def course_details():
    classid = flask.request.args.get("clsid")

    if classid == "" or classid is None:
        error_msg = "missing classid"
        html_code = flask.render_template("errorpage.html", error_msg =\
                                          error_msg)
        response = flask.make_response(html_code)
        return response

    try:
        isinstance(int(classid), int)
    except:
        error_msg = "non-integer classid"
        html_code = flask.render_template("errorpage.html", error_msg \
                                          = error_msg)
        response = flask.make_response(html_code)
        return response
    prev_classid = classid
    success, course_detail = DatabaseQuery.search_reg_details(classid)
    if success is not True:
        if course_detail == "no_class_id":
            error_msg = "no class with classid " + classid + " exists"
        else:
            error_msg = "A server error occured. Please contact the "+\
                "system administrator."
        html_code = flask.render_template("errorpage.html", error_msg\
                                          = error_msg)
        response = flask.make_response(html_code)
        return response
    html_code = flask.render_template("coursedetails.html",
        classid = classid,
        course_detail = course_detail)
    response = flask.make_response(html_code)
    response.set_cookie('prev_classid', prev_classid)
    return response