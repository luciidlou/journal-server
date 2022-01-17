CREATE TABLE `Entries` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` VARCHAR NOT NULL,
    `entry` VARCHAR NOT NULL,
    `mood_id` INTEGER NOT NULL,
    `date` TIMESTAMP NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `mood`(`id`)
);

CREATE TABLE `Moods` (
    `id` INTEGER NOT NULL PRIMARY KEY,
    `label` VARCHAR NOT NULL
);

INSERT INTO `Entries` VALUES (null, 'Python Decorators', 'I do not feel very comfortable with the @property decorator yet!', 3, 1601210007);
INSERT INTO `Entries` VALUES (null, 'SQL Queries', 'I have noticed that SQL queries read almost like plain english', 2, 1716251980);
INSERT INTO `Entries` VALUES (null, 'Python file structure', 'I am still trying to understand structuring directories and modules in Python ', 2, 1680508017);

INSERT INTO `Moods` VALUES (null, 'good');
INSERT INTO `Moods` VALUES (null, 'iffy');
INSERT INTO `Moods` VALUES (null, 'bad');