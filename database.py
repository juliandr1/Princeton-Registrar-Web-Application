import sys
import sqlite3
import contextlib
import course as coursemod
import coursedetails as detailmod

DATABASE_URL = 'file:reg.sqlite?mode=ro'

class DatabaseQuery:

    @staticmethod
    def search_reg(dept, num, area, title):
        try:
            with sqlite3.connect(
                    DATABASE_URL,
                    isolation_level = None,
                    uri = True) as connection:
                with contextlib.closing(connection.cursor()) as cursor:
                    input = []
                    stm_str = 'SELECT classid, dept, coursenum, area,'+\
                        ' title ' +\
                        'FROM classes, courses, crosslistings ' +\
                        'WHERE classes.courseid = courses.courseid ' +\
                        'AND courses.courseid = crosslistings.courseid'

                    if dept != "":
                        dept = '%' + dept.replace("%", "/%").replace\
                            ("_", "/_").upper() + '%'
                        stm_str += ' AND crosslistings.dept LIKE ?'
                        input.append(dept)
                    if num != "":
                        num = '%' + num.replace("%", "/%").replace\
                            ("_", "/_").upper() + '%'
                        stm_str += ' AND crosslistings.coursenum LIKE ?'
                        input.append(num)
                    if area != "":
                        area = '%' + area.replace("%", "/%").replace\
                            ("_", "/_").upper() + '%'
                        stm_str += ' AND courses.area LIKE ?'
                        input.append(area)

                    if title != "":
                        title = '%' + title.replace("%", "/%").replace\
                            ("_", "/_").upper() + '%'
                        stm_str += ' AND courses.title LIKE ?'
                        input.append(title)

                    if dept == "" and num == "" and area == "" \
                       and title == "":
                        stm_str += ' ORDER by dept, coursenum, classid'
                    else:
                        stm_str += ' ESCAPE "/" ORDER by dept, ' +\
                        'coursenum, classid'

                    cursor.execute(stm_str, input)
                    row = cursor.fetchone()
                    courses = []

                    while row is not None:

                        clsid  = str(row[0])
                        dept   = str(row[1])
                        crsnum = str(row[2])
                        area   = str(row[3])
                        title  = str(row[4])

                        course1 = coursemod.Course(
                            clsid,
                            dept,
                            crsnum,
                            area,
                            title)

                        courses.append(course1)
                        row = cursor.fetchone()

                    return True, courses

        except Exception as ex:
            print(ex, file = sys.stderr)
            return False, ex

    @staticmethod
    def search_reg_details(clsid):
        try:
            with sqlite3.connect(
                    DATABASE_URL,
                    isolation_level = None,
                    uri = True) as connection:
                with contextlib.closing(connection.cursor()) as cursor:

                    stm_str = 'SELECT classes.courseid, days, ' +\
                        'starttime, endtime, bldg, roomnum, dept,' +\
                        'coursenum, area, title, descrip, '+\
                        'prereqs, profname ' +\
                        'FROM classes, courses, crosslistings,' +\
                        'profs ' +\
                        'WHERE classes.courseid = courses.courseid ' +\
                        'AND courses.courseid = ' +\
                        'crosslistings.courseid ' +\
                        'AND classes.classid LIKE ? ORDER by dept,'+\
                        'coursenum'
                    cursor.execute(stm_str, [clsid])
                    row = cursor.fetchone()
                    if row is None:
                        return False, "no_class_id"
                    cls_details = []

                    cls_details.append(str(row[0]))
                    cls_details.append(str(row[1]))
                    cls_details.append(str(row[2]))
                    cls_details.append(str(row[3]))
                    cls_details.append(str(row[4]))
                    cls_details.append(str(row[5]))

                    stm = 'SELECT dept, coursenum, ' +\
                        'courses.courseid '+\
                        'FROM classes, crosslistings, courses '+ \
                        'WHERE classes.courseid = courses.courseid ' +\
                        'AND courses.courseid = ' +\
                        'crosslistings.courseid'+\
                        ' AND classes.classid LIKE ? '+\
                        'ORDER BY dept, coursenum'
                    cursor.execute(stm, [clsid])
                    row_str = cursor.fetchone()
                    depts = []

                    while row_str is not None:
                        dept = row_str[0] + " "
                        dept += str(row_str[1])
                        depts.append(dept)
                        row_str = cursor.fetchone()

                    crs_details = []
                    crs_details.append(str(row[8]))
                    crs_details.append(str(row[9]))
                    crs_details.append(str(row[10]))
                    crs_details.append(str(row[11]))

                    stmstr = 'SELECT coursesprofs.profid,' +\
                            'profname, classes.classid ' +\
                        'FROM coursesprofs, profs, classes ' +\
                        'WHERE coursesprofs.profid = profs.profid ' +\
                        'AND coursesprofs.courseid =' +\
                        'classes.courseid'+\
                        ' AND classes.classid LIKE ? Order by profname'

                    cursor.execute(stmstr, [clsid])
                    row_str = cursor.fetchone()
                    profs = []

                    while row_str is not None:
                        profs.append(str(row_str[1]))
                        row_str = cursor.fetchone()

                    details = detailmod.CourseDetails(
                            cls_details,
                            crs_details,
                            depts,
                            profs)

                    return True, details

        except Exception as ex:
            print(ex, file = sys.stderr)
            return False, ex