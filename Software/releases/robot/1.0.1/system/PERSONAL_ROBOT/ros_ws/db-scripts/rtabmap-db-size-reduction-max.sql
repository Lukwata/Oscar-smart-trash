
create view if not exists view_max_map_id as 
  select id from Node 
  where map_id <> (select max(map_id) from Node)
;

delete from Statistics where id in (select id from view_max_map_id);

delete from Data where id in (select id from view_max_map_id);

delete from Map_Node_Word where node_id in (select id from view_max_map_id);

delete from Link where from_id in (select id from view_max_map_id);

delete from Link where to_id in (select id from view_max_map_id);

delete from Node where map_id == (select min(map_id) from Node);

vacuum;
