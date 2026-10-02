insert into notecard(title, body) values ('clean kitchen','dishes,floor,etc');
insert into notecard(title, body) values ('mow','front, side. back');
insert into notecard(title, body) values ('print auto insurance card','');
insert into notecard(title, body) values ('laundry','whites, clothes, towels, washcloths, bedding');
insert into notecard(title, body) values ('add wiper fluid','');
insert into notecard(title, body) values ('check oil','');
insert into notecard(title, body) values ('check tires','');
insert into notecard(title, body) values ('wash car','');

insert into category(category,description) values ('car care','');
insert into category(category,description) values ('house work','');
insert into category(category,description) values ('chores','');
insert into category(category,description) values ('urgent','');
insert into category(category,description) values ('yard work','');

insert into notecard_category(notecard_id,category_id) values (
    (select notecard_id from notecard where title='clean kitchen'),
    (select category_id from category where category='house work')
);
