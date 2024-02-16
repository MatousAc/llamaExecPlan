set showplan_text on;
set showplan_text off;

-- query
select * 
from student s join attendance a on s.studentID = a.studentID
where s.race = 'Black or African American';
-- plan
-- Hash Match(Inner Join, HASH:(s.studentID)=(a.studentID))
-- Clustered Index Scan((student.PK_student AS s),  WHERE:(student.race as s.race=N'Black or African American'))
-- Clustered Index Scan(attendance.PK_attendance AS a)

select * from sys.dm_exec_query_stats;


select 	
	-- student info
	s.isFemale, s.isHispanic, s.raceCode,
	-- semester  data
	st.housingCode, st.gradeLvl, st.credits, st.tensOfHoursWorked,
	-- attendance data
	 a.distanceToFront, a.seatColumn, a.statusCode,
	-- section data
	sn.finalGradeCode, sn.finalGrade
from attendance a
	join student s on a.studentID = s.studentID 
	join studentTerm st on s.studentID = st.studentID
	join studentSection sn on s.studentID = sn.studentID and sn.termID = st.termID
	join section n on sn.sectionID = n.sectionID
	join event e on n.sectionID = e.sectionID and e.eventID = a.eventID
	join course c on n.courseID = c.courseID
where c.departmentID != 'NRSG' and c.departmentID != 'PEAC';

-- as one line:
select s.isFemale, s.isHispanic, s.raceCode, st.housingCode, st.gradeLvl, st.credits, st.tensOfHoursWorked, a.distanceToFront, a.seatColumn, a.statusCode, sn.finalGradeCode, sn.finalGrade from attendance a join student s on a.studentID = s.studentID  join studentTerm st on s.studentID = st.studentID join studentSection sn on s.studentID = sn.studentID and sn.termID = st.termID join section n on sn.sectionID = n.sectionID join event e on n.sectionID = e.sectionID and e.eventID = a.eventID join course c on n.courseID = c.courseID where c.departmentID != 'NRSG' and c.departmentID != 'PEAC';
