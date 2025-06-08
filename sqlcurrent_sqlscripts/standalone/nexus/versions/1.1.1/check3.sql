drop function if exists checkfunction();

create or replace function checkfunction () returns table (script_failed integer, script_failed_reason varchar(256)) as $$
declare
	script_failed integer = 0;
	script_failed_reason varchar(256) = '';
	record_count integer;
begin
	select count(*) into record_count from sqlcurrent_a;

	if record_count > 0 then
		script_failed = 1;
		script_failed_reason = 'Records found in table sqlcurrent_a.  This table should be empty.';
		return query select script_failed, script_failed_reason;
	end if;

	return query select script_failed, script_failed_reason;
end;
$$ language plpgsql;

select * from checkfunction();
