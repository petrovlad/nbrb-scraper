create table currency (
  id int primary key auto_increment,
  full_name varchar(50),
  abbreviation varchar(10) unique
);

create table course_stat (
  stat_id int primary key auto_increment,
  stat_date Date,
  curr_id int references currency,
  curr_amount float,
  curr_course float
);
