# Student Management System
A Web-based system to record student registration and grade information for courses at a university.

FUNCTIONALITIES OF THE PROJECT

Users:
1)	Student
2)	Faculty
3)	Administrator
Roles:
	Student: 

1)	Login their respective account with their credentials. 
 
![image](https://github.com/user-attachments/assets/5156bd44-606b-4c6f-b396-07b2de4542d3)
![image](https://github.com/user-attachments/assets/5c74922d-a55c-447a-bed1-7584933c8a1f)

2)	View their registered courses and grades of courses if the course has been graded by the faculty.
![image](https://github.com/user-attachments/assets/c6da680f-0c93-41c8-929e-2bf6f2adb8ef)

3)	Change Password of their account.
![image](https://github.com/user-attachments/assets/da195e20-cbb6-4cb8-ad5f-6997e5eb6856)

	Faculty: 

1)	Login their respective account with their credentials.
![image](https://github.com/user-attachments/assets/500823a8-9c81-4c3e-8347-6a95e3420a97)![image](https://github.com/user-attachments/assets/f9a26975-952e-47a1-97cc-0794824777c4)

2)	View his/her instructing courses and their respective strength of the current batch.
![image](https://github.com/user-attachments/assets/22d1a84d-df34-4b3b-9660-ce620e30fc79)

3)	Change Password for his/her account.
![image](https://github.com/user-attachments/assets/b809adb7-c70f-40a5-986c-ef5358833fb1)
4)	View students of all batches for a particular course.
 ![image](https://github.com/user-attachments/assets/f4e6b245-1268-4971-97ff-181c59e8affc)

5)	Grade all students of the course of which Grading is allowed.
 ![image](https://github.com/user-attachments/assets/9d0cc19e-7199-4014-8952-65ce5ab4d6f9)

6)	Freeze and submit the assigned grades of the student.
![image](https://github.com/user-attachments/assets/4dd17234-c872-4512-8a78-09514c90b445)

	Admin:

1)	Login with their credentials.
![image](https://github.com/user-attachments/assets/9a9d752b-05e2-45f5-ac1e-1b4f25f42f34)

2)	Use admin features such for different functionalities for Students, Faculties, Courses and Gradings.
![image](https://github.com/user-attachments/assets/3fa1d350-345e-4f63-9616-ac82d8cc1069)

Administrator Features

Administrator has different features to perform on Students, Faculties, Courses and Gradings.
	Student

1)	Add a new Student.
![image](https://github.com/user-attachments/assets/cb924e26-5649-4076-a321-e1d56546491b)

2)	Register a course to a particular Student based on the Courses offered by their respective Departments.
![image](https://github.com/user-attachments/assets/352c9b42-404f-444d-b2e6-492bb488e50f)

3)	View all Registered Students.
![image](https://github.com/user-attachments/assets/ac04e3b5-5f6f-4ec0-9bfc-da032593031d)

	Faculty

1)	Add a new Faculty.
![image](https://github.com/user-attachments/assets/e65c6b57-3ded-4660-8789-d03db5fa6518)

2)	Allocate a course to a particular Faculty based on the Courses offered by their respective Departments.
![image](https://github.com/user-attachments/assets/21301eab-6989-4d91-a6de-d9bf5de762a2)

3)	View all Registered Faculties.
![image](https://github.com/user-attachments/assets/5b925f65-ad2c-408a-888a-583e64304c5c)

	Course

1)	Add a new Course.
![image](https://github.com/user-attachments/assets/4fc83cf9-682e-4fa8-9191-b21f8b8107d3)

2)	View all Courses.
![image](https://github.com/user-attachments/assets/44349782-f87a-402f-99b2-c39399b35722)

	Grading

1)	Grade all Courses whose Registration is no more open.
![image](https://github.com/user-attachments/assets/1400feb4-a504-47b9-90fc-31e18524a015)

PROJECT-DIRECTORY STRUCTURE
![image](https://github.com/user-attachments/assets/af735b71-a254-4ee2-acc4-5636c2b1c9d9)
	
UNIQUENESS OF THE PROJECT

1.	Run time user-type identification.
	Use of HTTP Session variable to implement run time user-type identification to login authentication for Students and Faculties.
2.	Identifying the submitted data using common named HTML attributes.
	Use of HTML button’s dynamically generated value attribute to identify same named select attribute to fetch data from forms.
3.	Dynamic name assignment to HTML attributes.
	Use of Jinja2 to dynamically assign names for HTML attributes using data from back-end.
4.	NO JAVASCRIPT CODE (Ignoring Bootstrap JS linkages).
	Python, HTML and Bootstrap are only used for entire web functionality.
5.	Lightweight Tech-stack for quick start development.
	Flask, SQLite and Bootstrap are easy and quick to start frameworks and timely project submission.
6.	Optimized data storage (No redundant attributes).
	Efficient use of keys (Primary and Foreign keys) to reduce redundant attributes across all tables of the database.

