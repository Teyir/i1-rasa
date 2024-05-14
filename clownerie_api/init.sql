CREATE TABLE IF NOT EXISTS `booking`
(
    `booking_id`           int(11)      NOT NULL AUTO_INCREMENT,
    `booking_code`         varchar(255) NOT NULL,
    `booking_phone`        int(255)     NOT NULL,
    `booking_restaurant`   int(11)      NOT NULL,
    `booking_date`         timestamp    NOT NULL DEFAULT current_timestamp(),
    `booking_commentary`   text         NOT NULL,
    `booking_date_created` timestamp    NOT NULL DEFAULT current_timestamp(),
    `booking_date_updated` timestamp    NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
    `booking_date_status`  tinyint(4)   NOT NULL DEFAULT 1 COMMENT '1 = booked\r\n0 = canceled',
    PRIMARY KEY (`booking_id`),
    UNIQUE KEY `booking_code` (`booking_code`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COLLATE = utf8_general_ci;
