use Titan;

create table duplicate_files_hash (
	`id_duplicate_file` INT NOT NULL AUTO_INCREMENT,
        `file_hash` VARCHAR(64) NOT NULL,
        `host_name` VARCHAR(256) NOT NULL,
	`file_location` VARCHAR(512) NOT NULL,
        PRIMARY KEY (`id_duplicate_file`)
);
