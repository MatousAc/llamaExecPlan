use attendanceDB;
set showplan_text on;
set showplan_text off;

-- queries
-- selects african american students
select * from student s join attendance a on s.studentID = a.studentID where s.race = 'Black or African American';
-- selects all relevant information alongside every attendance record
select s.isFemale, s.isHispanic, s.raceCode, st.housingCode, st.gradeLvl, st.credits, st.tensOfHoursWorked, a.distanceToFront, a.seatColumn, a.statusCode, sn.finalGradeCode, sn.finalGrade from attendance a join student s on a.studentID = s.studentID  join studentTerm st on s.studentID = st.studentID join studentSection sn on s.studentID = sn.studentID and sn.termID = st.termID join section n on sn.sectionID = n.sectionID join event e on n.sectionID = e.sectionID and e.eventID = a.eventID join course c on n.courseID = c.courseID where c.departmentID != 'NRSG' and c.departmentID != 'PEAC';
-- selects terms where students didn't attend
select distinct t.startDate from term t join studentSection ss on t.termID = ss.termID where noAttenceFlag = 'False';
-- selects students who brought their grades up between midterm and finals
select s.gender, s.raceCode, s.standardTestScore from student s join studentSection ss on s.studentID = ss.studentID where ss.midtermGrade = 'F' and ss.finalGrade = 'A';
select s.gender, s.raceCode, s.standardTestScore from student s join studentSection ss on s.studentID = ss.studentID where ss.midtermGrade = 'D' and ss.finalGrade = 'B';
-- get depts
select * from department;
-- select professors who taught in specific depts
select p.professorName from professor p join section s on p.professorID = s.professorID join course c on s.courseID = c.courseID join department d on c.departmentID = d.departmentID where d.departmentName = 'Computing' or d.departmentName = 'Physics';
-- get average course credits in various ways
select avg(c.credits) as 'creditAverage' from course c;
select d.departmentName, avg(c.credits) as 'creditAverage' from course c join department d on c.departmentID = d.departmentID group by d.departmentName;
select avg(c.credits) as 'creditAverage' from section se join course c on se.courseID = c.courseID;
-- get rooms
select building, roomNumber from room;
-- professors who taught in specific places
select p.professorName, r.roomNumber from professor p join section se on p.professorID = se.professorID join room r on se.roomID = r.roomID where r.building = 'Hickman Science Center';
-- group by building
select p.professorName, r.building, count(r.roomNumber) as 'numberOfRooms' from professor p join section se on p.professorID = se.professorID join room r on se.roomID = r.roomID group by r.building, p.professorName;
-- class and professor with highest/lowest avg
select top 5 p.professorName, concat(c.courseCode, '-', se.sectionLetter), avg(sse.finalGradeCode) as 'classGrade' from professor p join section se on p.professorID = se.professorID join studentSection sse on se.sectionID = sse.sectionID join course c on se.courseID = c.courseID group by p.professorName, se.sectionLetter, c.courseCode order by avg(sse.finalGradeCode) asc;
select top 5 p.professorName, concat(c.courseCode, '-', se.sectionLetter), avg(sse.finalGradeCode) as 'classGrade' from professor p join section se on p.professorID = se.professorID join studentSection sse on se.sectionID = sse.sectionID join course c on se.courseID = c.courseID group by p.professorName, se.sectionLetter, c.courseCode order by avg(sse.finalGradeCode) desc;
-- professor's average student grades
select p.professorName, avg(sse.finalGradeCode) as 'avgGrade' from professor p join section se on p.professorID = se.professorID join studentSection sse on se.sectionID = sse.sectionID group by p.professorName;
