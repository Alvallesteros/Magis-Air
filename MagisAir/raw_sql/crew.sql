BEGIN;
--
-- Create model CrewMember
--
CREATE TABLE "app_crew_crewmember" (
  "crew_member_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "last_name" varchar(255) NOT NULL, 
  "first_name" varchar(255) NOT NULL, 
  "middle_initial" varchar(5) NULL
);
--
-- Create model CrewAssignment
--
CREATE TABLE "app_crew_crewassignment" (
  "crew_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "role" varchar(20) NOT NULL, 
  "crew_member_id" integer NOT NULL REFERENCES "app_crew_crewmember" ("crew_member_id") DEFERRABLE INITIALLY DEFERRED, 
  "scheduled_flight_id" integer NOT NULL REFERENCES "app_schedule_scheduledflight" ("scheduled_flight_id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "app_crew_crewassignment_crew_member_id_174af812" ON "app_crew_crewassignment" ("crew_member_id");
CREATE INDEX "app_crew_crewassignment_scheduled_flight_id_ff782a38" ON "app_crew_crewassignment" ("scheduled_flight_id");
COMMIT;
