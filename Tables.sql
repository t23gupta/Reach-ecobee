CREATE TABLE employee_details 
	(ID int auto_increment primary key, Employee_Name varchar(255), Job_Title varchar(255), Description text);
    
CREATE TABLE employee_interests_normalized
	(ID int auto_increment primary key, Employee_ID int, Employee_Name varchar(255), Interest varchar(255));
    
