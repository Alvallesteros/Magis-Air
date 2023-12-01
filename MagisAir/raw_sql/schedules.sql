BEGIN;
--
-- Create model ScheduledFlight
--
CREATE TABLE "app_schedule_scheduledflight" (
  "scheduled_flight_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "departure_date" date NOT NULL, 
  "departure_time" time NOT NULL, 
  "arrival_date" date NOT NULL, 
  "arrival_time" time NOT NULL, 
  "duration" varchar(10) NOT NULL, 
  "flight_cost" real NOT NULL, 
  "base_flight_id" bigint NOT NULL REFERENCES "app_routes_baseflight" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX "app_schedule_scheduledflight_base_flight_id_d84b859a" ON "app_schedule_scheduledflight" ("base_flight_id");
COMMIT;
