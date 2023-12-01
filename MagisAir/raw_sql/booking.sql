BEGIN;
--
-- Create model Booking
--
CREATE TABLE "app_booking_booking" (
  "booking_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "booking_date" date NOT NULL, 
  "booking_time" time NOT NULL, 
  "total_cost" decimal NOT NULL
);
--
-- Create model Item
--
CREATE TABLE "app_booking_item" (
  "item_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "description" varchar(255) NOT NULL, 
  "item_cost" decimal NOT NULL
);
--
-- Create model Passenger
--
CREATE TABLE "app_booking_passenger" (
  "passenger_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "last_name" varchar(255) NOT NULL,
  "first_name" varchar(255) NOT NULL, 
  "middle_initial" varchar(1) NULL, 
  "birthday" date NOT NULL, 
  "gender" varchar(1) NOT NULL
);
--
-- Create model Ticket
--
CREATE TABLE "app_booking_ticket" (
  "ticket_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "seat_class" varchar(100) NOT NULL, 
  "seat_number" varchar(3) NOT NULL, 
  "ticket_cost" decimal NOT NULL, 
  "booking_id" integer NOT NULL REFERENCES "app_booking_booking" ("booking_id") DEFERRABLE INITIALLY DEFERRED, 
  "scheduled_flight_id" integer NOT NULL REFERENCES "app_schedule_scheduledflight" ("scheduled_flight_id") DEFERRABLE INITIALLY DEFERRED
);
--
-- Create model BookingItem
--
CREATE TABLE "app_booking_bookingitem" (
  "booking_item_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "item_quantity" integer NOT NULL, "booking_item_cost" decimal NOT NULL, 
  "booking_id" integer NOT NULL REFERENCES "app_booking_booking" ("booking_id") DEFERRABLE INITIALLY DEFERRED, 
  "item_id" integer NOT NULL REFERENCES "app_booking_item" ("item_id") DEFERRABLE INITIALLY DEFERRED
);
--
-- Add field passenger to booking
--
CREATE TABLE "new__app_booking_booking" (
  "booking_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  "booking_date" date NOT NULL, 
  "booking_time" time NOT NULL, 
  "total_cost" decimal NOT NULL, 
  "passenger_id" integer NOT NULL REFERENCES "app_booking_passenger" ("passenger_id") DEFERRABLE INITIALLY DEFERRED
);

INSERT INTO "new__app_booking_booking" (
  "booking_id", 
  "booking_date", 
  "booking_time", 
  "total_cost", 
  "passenger_id"
) 
  SELECT 
    "booking_id", 
    "booking_date", 
    "booking_time", 
    "total_cost", 
    NULL FROM "app_booking_booking";

DROP TABLE "app_booking_booking";
ALTER TABLE "new__app_booking_booking" RENAME TO "app_booking_booking";
CREATE INDEX "app_booking_ticket_booking_id_6330e94a" ON "app_booking_ticket" ("booking_id");
CREATE INDEX "app_booking_ticket_scheduled_flight_id_88c1074a" ON "app_booking_ticket" ("scheduled_flight_id");
CREATE INDEX "app_booking_bookingitem_booking_id_2bdb3580" ON "app_booking_bookingitem" ("booking_id");
CREATE INDEX "app_booking_bookingitem_item_id_f5464b58" ON "app_booking_bookingitem" ("item_id");
CREATE INDEX "app_booking_booking_passenger_id_660e4a07" ON "app_booking_booking" ("passenger_id");
COMMIT;
