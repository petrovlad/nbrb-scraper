create table currency_stat (
  stat_id int primary key auto_increment,
  stat_date Date,
  curr_name varchar(50),
  curr_amount varchar(10),
  curr_course float
)
