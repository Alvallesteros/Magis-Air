BEGIN;
--
-- Create model Route
--
CREATE TABLE "app_routes_route" (
  "route_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "origin" varchar(255) NOT NULL, 
  "destination" varchar(255) NOT NULL
);
--
-- Create model BaseFlight
--
CREATE TABLE "app_routes_baseflight" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "flight_code" varchar(6) NOT NULL UNIQUE, 
  "flight_type" varchar(20) NOT NULL, 
  "route_id" integer NOT NULL REFERENCES 
  "app_routes_route" ("route_id") DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX "app_routes_baseflight_route_id_d4090b1f" ON "app_routes_baseflight" ("route_id");
COMMIT;
