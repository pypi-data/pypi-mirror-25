create table `artist` (
	`artistid` integer AUTO_INCREMENT,
	`name` text,
	constraint `pk_artist` primary key (`artistid`),
	constraint `artist_unique0` unique (`name`)
) ENGINE=MyISAM;
create table `track` (
	`trackid` integer AUTO_INCREMENT,
	`cdid` integer,
	`title` text,
	constraint `pk_track` primary key (`trackid`),
	constraint `track_unique0` unique (`title`, `cdid`),
	constraint `fk_track_cd` foreign key (`cdid`) references `cd` (`cdid`)
) ENGINE=MyISAM;
create table `cd` (
	`cdid` integer AUTO_INCREMENT,
	`year` timestamp null,
	`artistid` integer,
	`title` text,
	constraint `pk_cd` primary key (`cdid`),
	constraint `cd_unique0` unique (`title`, `artistid`),
	constraint `fk_cd_artist` foreign key (`artistid`) references `artist` (`artistid`)
) ENGINE=MyISAM;