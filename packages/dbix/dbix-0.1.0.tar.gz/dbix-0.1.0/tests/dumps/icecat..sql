
	PRAGMA recursive_triggers=1;
	;
create table [category_feature] (
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[mandatory] integer default (0) null,
	[catid] integer,
	[searchable] integer default (0),
	[no] integer default (0),
	[category_feature_id] integer,
	[restricted_search_values] text null,
	[feature_id] integer,
	[use_dropdown_input] char(3) default ('') null,
	[category_feature_group_id] integer default (0),
	constraint [pk_category_feature] primary key ([category_feature_id]),
	constraint [category_feature_unique0] unique ([feature_id], [catid]),
	constraint [category_feature_unique1] unique ([feature_id], [catid]),
	constraint [fk_category_feature_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_category_feature_category_feature_group] foreign key ([category_feature_group_id]) references [category_feature_group] ([category_feature_group_id]),
	constraint [fk_category_feature_feature] foreign key ([feature_id]) references [feature] ([feature_id]),
	constraint [fk_category_feature_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_category_feature_category_feature_group] foreign key ([category_feature_group_id]) references [category_feature_group] ([category_feature_group_id]),
	constraint [fk_category_feature_feature] foreign key ([feature_id]) references [feature] ([feature_id])
) ;

		create trigger [tr_category_feature0] 
		after update 
		of [mandatory], [catid], [searchable], [no], [category_feature_id], [restricted_search_values], [feature_id], [use_dropdown_input], [category_feature_group_id] 
		on [category_feature] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [category_feature] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[category_feature_id]=[category_feature_id];
		end;
		;
create table [product_review] (
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[review_code] varchar(60) default (''),
	[review_group] varchar(60) default (''),
	[review_id] integer default (0),
	[product_review_id] integer primary key autoincrement,
	[url] varchar(255) default (''),
	[high_review_award_url] varchar(255) default (''),
	[value] text null,
	[langid] integer default (0),
	[review_award_name] varchar(120) default (''),
	[postscriptum] text null,
	[score] integer default (0),
	[value_bad] text null,
	[date_added] date default (strftime('%Y-%m-%d', 'now')),
	[value_good] text null,
	[product_id] integer,
	[logo_url] varchar(255) default (''),
	[low_review_award_url] varchar(255) default ('') not null,
	constraint [product_review_unique0] unique ([product_id], [review_id], [langid]),
	constraint [product_review_unique1] unique ([product_id], [review_id], [langid]),
	constraint [fk_product_review_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_product_review_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_review_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_product_review_product] foreign key ([product_id]) references [product] ([product_id])
) ;

		create trigger [tr_product_review0] 
		after update 
		of [review_code], [review_group], [review_id], [product_review_id], [url], [high_review_award_url], [value], [langid], [review_award_name], [postscriptum], [score], [value_bad], [date_added], [value_good], [product_id], [logo_url], [low_review_award_url] 
		on [product_review] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [product_review] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[product_review_id]=[product_review_id];
		end;
		;
create table [product_family] (
	[thumb_pic] varchar(255) null,
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[supplier_id] integer,
	[catid] integer null,
	[symbol] varchar(120) default (''),
	[low_pic] varchar(255) null,
	[family_id] integer,
	[sid] integer,
	[tid] integer,
	[parent_family_id] integer null,
	[data_source_id] integer default (0),
	constraint [pk_product_family] primary key ([family_id]),
	constraint [fk_product_family_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_product_family_parent] foreign key ([parent_family_id]) references [product_family] ([family_id]),
	constraint [fk_product_family_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_product_family_supplier] foreign key ([supplier_id]) references [supplier] ([supplier_id]),
	constraint [fk_product_family_tidindex] foreign key ([tid]) references [tid_index] ([tid]),
	constraint [fk_product_family_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_product_family_parent] foreign key ([parent_family_id]) references [product_family] ([family_id]),
	constraint [fk_product_family_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_product_family_supplier] foreign key ([supplier_id]) references [supplier] ([supplier_id]),
	constraint [fk_product_family_tidindex] foreign key ([tid]) references [tid_index] ([tid])
) ;

		create trigger [tr_product_family0] 
		after update 
		of [thumb_pic], [supplier_id], [catid], [symbol], [low_pic], [family_id], [sid], [tid], [parent_family_id], [data_source_id] 
		on [product_family] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [product_family] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[family_id]=[family_id];
		end;
		;
create table [feature_logo_category] (
	[feature_logo_id] integer,
	[category_id] integer,
	constraint [pk_feature_logo_category] primary key ([feature_logo_id], [category_id]),
	constraint [fk_feature_logo_category_feature_logo] foreign key ([feature_logo_id]) references [feature_logo] ([feature_logo_id]),
	constraint [fk_feature_logo_category_category] foreign key ([category_id]) references [category] ([catid]),
	constraint [fk_feature_logo_category_feature_logo] foreign key ([feature_logo_id]) references [feature_logo] ([feature_logo_id]),
	constraint [fk_feature_logo_category_category] foreign key ([category_id]) references [category] ([catid])
) ;
create table [feature] (
	[measure_id] integer null,
	[last_published] integer default (0) null,
	[searchable] integer default (0),
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[feature_id] integer,
	[tid] integer,
	[sid] integer,
	[limit_direction] integer default (0),
	[restricted_values] text null,
	[type] varchar(60),
	[class] integer default (0),
	constraint [pk_feature] primary key ([feature_id]),
	constraint [fk_feature_measure] foreign key ([measure_id]) references [measure] ([measure_id]),
	constraint [fk_feature_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_feature_tidindex] foreign key ([tid]) references [tid_index] ([tid]),
	constraint [fk_feature_measure] foreign key ([measure_id]) references [measure] ([measure_id]),
	constraint [fk_feature_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_feature_tidindex] foreign key ([tid]) references [tid_index] ([tid])
) ;

		create trigger [tr_feature0] 
		after update 
		of [measure_id], [last_published], [searchable], [feature_id], [tid], [sid], [limit_direction], [restricted_values], [type], [class] 
		on [feature] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [feature] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[feature_id]=[feature_id];
		end;
		;
create table [measure_sign] (
	[measure_id] integer,
	[last_published] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[measure_sign_id] integer,
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[value] varchar(255),
	[langid] integer,
	constraint [pk_measure_sign] primary key ([measure_sign_id]),
	constraint [measure_sign_unique0] unique ([measure_id], [langid]),
	constraint [measure_sign_unique1] unique ([measure_id], [langid]),
	constraint [fk_measure_sign_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_measure_sign_measure] foreign key ([measure_id]) references [measure] ([measure_id]),
	constraint [fk_measure_sign_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_measure_sign_measure] foreign key ([measure_id]) references [measure] ([measure_id])
) ;

		create trigger [tr_measure_sign0] 
		after update 
		of [measure_id], [last_published], [measure_sign_id], [value], [langid] 
		on [measure_sign] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [measure_sign] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[measure_sign_id]=[measure_sign_id];
		end;
		;
create table [tex] (
	[tid] integer,
	[tex_id] integer,
	[langid] integer default (0),
	[value] text,
	constraint [pk_tex] primary key ([tex_id]),
	constraint [tex_unique0] unique ([tid], [langid]),
	constraint [tex_unique1] unique ([tid], [langid]),
	constraint [fk_tex_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_tex_tidindex] foreign key ([tid]) references [tid_index] ([tid]),
	constraint [fk_tex_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_tex_tidindex] foreign key ([tid]) references [tid_index] ([tid])
) ;
create table [supplier] (
	[thumb_pic] varchar(255) null,
	[has_vendor_index] integer default (0),
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[supplier_id] integer,
	[user_id] integer default (1),
	[name] varchar(255) default (''),
	[acknowledge] char(1) default ('N'),
	[public_login] varchar(80) default ('') null,
	[hide_products] integer default (0),
	[suppress_offers] char(1) default ('N'),
	[low_pic] varchar(255) null,
	[public_password] varchar(80) default ('') null,
	[last_name] varchar(255) default (''),
	[folder_name] varchar(255) default (''),
	[template] text null,
	[is_sponsor] char(1) default ('N'),
	[prod_id_regexp] text null,
	[ftp_homedir] varchar(255) null,
	[last_published] integer default (0) null,
	constraint [pk_supplier] primary key ([supplier_id]),
	constraint [name] unique ([name]),
	constraint [name] unique ([name])
) ;

		create trigger [tr_supplier0] 
		after update 
		of [thumb_pic], [has_vendor_index], [supplier_id], [user_id], [name], [acknowledge], [public_login], [hide_products], [suppress_offers], [low_pic], [public_password], [last_name], [folder_name], [template], [is_sponsor], [prod_id_regexp], [ftp_homedir], [last_published] 
		on [supplier] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [supplier] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[supplier_id]=[supplier_id];
		end;
		;
create table [feature_logo] (
	[thumb_link] varchar(255) default (''),
	[feature_logo_id] integer primary key autoincrement,
	[height] integer,
	[feature_id] integer,
	[width] integer,
	[link] varchar(255),
	[thumb_size] integer default (0),
	[values] varchar(255) default (''),
	[size] integer,
	constraint [feature_logo_unique0] unique ([link]),
	constraint [feature_logo_unique1] unique ([link]),
	constraint [fk_feature_logo_feature] foreign key ([feature_id]) references [feature] ([feature_id]),
	constraint [fk_feature_logo_feature] foreign key ([feature_id]) references [feature] ([feature_id])
) ;
create table [tid_index] (
	[tid] integer primary key autoincrement,
	[dummy] smallint null
) ;
create table [product_multimedia_object] (
	[keep_as_url] integer,
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[uuid] varchar(40),
	[width] integer,
	[type] varchar(255),
	[is_rich] integer,
	[preview_url] varchar(255),
	[preview_height] integer,
	[langid] integer,
	[height] integer,
	[source] varchar(255),
	[product_id] integer,
	[link] varchar(255),
	[size] integer,
	[content_type] varchar(255),
	[preview_width] integer,
	[thumb_url] varchar(255),
	[preview_size] integer,
	[id] integer primary key autoincrement,
	[description] text,
	constraint [product_multimedia_object_unique0] unique ([product_id], [langid], [link]),
	constraint [product_multimedia_object_unique1] unique ([product_id], [langid], [link]),
	constraint [fk_product_multimedia_object_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_multimedia_object_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_product_multimedia_object_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_multimedia_object_language] foreign key ([langid]) references [language] ([langid])
) ;

		create trigger [tr_product_multimedia_object0] 
		after update 
		of [keep_as_url], [uuid], [width], [type], [is_rich], [preview_url], [preview_height], [langid], [height], [source], [product_id], [link], [size], [content_type], [preview_width], [thumb_url], [preview_size], [id], [description] 
		on [product_multimedia_object] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [product_multimedia_object] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[id]=[id];
		end;
		;
create table [product] (
	[topseller] varchar(255) default (''),
	[prod_id] varchar(60) default (''),
	[low_pic] varchar(255) default (''),
	[got_images] integer default (1),
	[medium_pic] varchar(255) default (''),
	[gtin] varchar(14) null,
	[quality] varchar(16),
	[supplier_id] integer,
	[user_id] integer default (1),
	[catid] integer default (0),
	[high_pic_size] integer default (0) null,
	[publish] char(1) default ('Y'),
	[thumb_pic_size] integer default (0) null,
	[launch_date] timestamp null,
	[public] char(1) default ('Y'),
	[thumb_pic] varchar(255) null,
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[medium_pic_width] integer default (0),
	[medium_pic_height] integer default (0),
	[low_pic_size] integer default (0) null,
	[high_pic] varchar(255) default (''),
	[high_pic_origin_size] integer default (0),
	[series_id] integer default (1),
	[low_pic_width] integer default (0),
	[low_pic_height] integer default (0),
	[date_added] date default (strftime('%Y-%m-%d', 'now')),
	[product_id] integer,
	[high_pic_origin] varchar(255) default (''),
	[medium_pic_size] integer default (0),
	[name] varchar(255) default (''),
	[on_market] integer default (1),
	[dname] varchar(255) default (''),
	[high_pic_width] integer default (0),
	[checked_by_supereditor] integer default (0),
	[family_id] integer default (0),
	[high_pic_height] integer default (0),
	[obsolence_date] integer null,
	constraint [pk_product] primary key ([product_id]),
	constraint [product_unique0] unique ([prod_id], [supplier_id]),
	constraint [product_unique1] unique ([prod_id], [supplier_id]),
	constraint [fk_product_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_product_supplier] foreign key ([supplier_id]) references [supplier] ([supplier_id]),
	constraint [fk_product_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_product_supplier] foreign key ([supplier_id]) references [supplier] ([supplier_id])
) ;

		create trigger [tr_product0] 
		after update 
		of [topseller], [prod_id], [low_pic], [got_images], [medium_pic], [gtin], [quality], [supplier_id], [user_id], [catid], [high_pic_size], [publish], [thumb_pic_size], [launch_date], [public], [thumb_pic], [medium_pic_width], [medium_pic_height], [low_pic_size], [high_pic], [high_pic_origin_size], [series_id], [low_pic_width], [low_pic_height], [date_added], [product_id], [high_pic_origin], [medium_pic_size], [name], [on_market], [dname], [high_pic_width], [checked_by_supereditor], [family_id], [high_pic_height], [obsolence_date] 
		on [product] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [product] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[product_id]=[product_id];
		end;
		;
create table [feature_group] (
	[feature_group_id] integer,
	[sid] integer,
	constraint [pk_feature_group] primary key ([feature_group_id]),
	constraint [fk_feature_group_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_feature_group_sidindex] foreign key ([sid]) references [sid_index] ([sid])
) ;
create table [category_keywords] (
	[keywords] text null,
	[category_id] integer null,
	[langid] integer default (0),
	[id] integer,
	constraint [pk_category_keywords] primary key ([id]),
	constraint [category_keywords_unique0] unique ([langid], [category_id]),
	constraint [category_keywords_unique1] unique ([langid], [category_id]),
	constraint [fk_category_keywords_category] foreign key ([category_id]) references [category] ([catid]),
	constraint [fk_category_keywords_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_category_keywords_category] foreign key ([category_id]) references [category] ([catid]),
	constraint [fk_category_keywords_language] foreign key ([langid]) references [language] ([langid])
) ;
create table [product_related] (
	[preferred_option] integer default (0),
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[product_id] integer,
	[rel_product_id] integer,
	[product_related_id] integer primary key autoincrement,
	[order] smallint default (0),
	[data_source_id] integer default (0),
	constraint [product_related_unique0] unique ([product_id], [rel_product_id]),
	constraint [product_related_unique1] unique ([product_id], [rel_product_id]),
	constraint [fk_product_related_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_related_related_product] foreign key ([rel_product_id]) references [product] ([product_id]),
	constraint [fk_product_related_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_related_related_product] foreign key ([rel_product_id]) references [product] ([product_id])
) ;

		create trigger [tr_product_related0] 
		after update 
		of [preferred_option], [product_id], [rel_product_id], [product_related_id], [order], [data_source_id] 
		on [product_related] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [product_related] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[product_related_id]=[product_related_id];
		end;
		;
create table [product_feature_local] (
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[product_id] integer default (0),
	[product_feature_local_id] integer primary key autoincrement,
	[category_feature_id] integer default (0),
	[langid] integer default (0),
	[value] varchar(15000) default (''),
	constraint [product_feature_local_unique0] unique ([category_feature_id], [product_id], [langid]),
	constraint [product_feature_local_unique1] unique ([category_feature_id], [product_id], [langid]),
	constraint [fk_product_feature_local_category_feature] foreign key ([category_feature_id]) references [category_feature] ([category_feature_id]),
	constraint [fk_product_feature_local_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_product_feature_local_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_feature_local_category_feature] foreign key ([category_feature_id]) references [category_feature] ([category_feature_id]),
	constraint [fk_product_feature_local_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_product_feature_local_product] foreign key ([product_id]) references [product] ([product_id])
) ;

		create trigger [tr_product_feature_local0] 
		after update 
		of [product_id], [product_feature_local_id], [category_feature_id], [langid], [value] 
		on [product_feature_local] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [product_feature_local] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[product_feature_local_id]=[product_feature_local_id];
		end;
		;
create table [product_gallery] (
	[thumb_link] varchar(255),
	[height] integer,
	[got_images] integer default (1),
	[logo] integer,
	[id] integer primary key autoincrement,
	[size] integer,
	[medium_size] integer,
	[no] integer,
	[low_link] varchar(255),
	[low_height] integer,
	[size_origin] integer,
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[low_size] integer,
	[link] varchar(255),
	[low_width] integer,
	[product_id] integer,
	[medium_width] integer,
	[medium_link] varchar(255),
	[langid] integer,
	[medium_height] integer,
	[source] varchar(255),
	[thumb_size] integer,
	[width] integer,
	[is_main] integer,
	constraint [product_gallery_unique0] unique ([product_id], [link]),
	constraint [product_gallery_unique1] unique ([product_id], [link]),
	constraint [fk_product_gallery_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_product_gallery_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_gallery_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_product_gallery_product] foreign key ([product_id]) references [product] ([product_id])
) ;

		create trigger [tr_product_gallery0] 
		after update 
		of [thumb_link], [height], [got_images], [logo], [id], [size], [medium_size], [no], [low_link], [low_height], [size_origin], [low_size], [link], [low_width], [product_id], [medium_width], [medium_link], [langid], [medium_height], [source], [thumb_size], [width], [is_main] 
		on [product_gallery] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [product_gallery] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[id]=[id];
		end;
		;
create table [measure] (
	[measure_id] integer,
	[last_published] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[sign] varchar(255) null,
	[sid] integer,
	[tid] integer,
	[system_of_measurement] varchar default ('metric'),
	constraint [check0] check ([system_of_measurement] in ('metric','imperial')),
	constraint [pk_measure] primary key ([measure_id]),
	constraint [fk_measure_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_measure_tidindex] foreign key ([tid]) references [tid_index] ([tid]),
	constraint [fk_measure_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_measure_tidindex] foreign key ([tid]) references [tid_index] ([tid])
) ;

		create trigger [tr_measure0] 
		after update 
		of [measure_id], [last_published], [sign], [sid], [tid], [system_of_measurement] 
		on [measure] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [measure] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[measure_id]=[measure_id];
		end;
		;
create table [product_feature] (
	[product_feature_id] integer primary key autoincrement,
	[category_feature_id] integer,
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[value] varchar(20000) default (''),
	[product_id] integer,
	constraint [product_feature_unique0] unique ([category_feature_id], [product_id]),
	constraint [product_feature_unique1] unique ([category_feature_id], [product_id]),
	constraint [fk_product_feature_category_feature] foreign key ([category_feature_id]) references [category_feature] ([category_feature_id]),
	constraint [fk_product_feature_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_feature_category_feature] foreign key ([category_feature_id]) references [category_feature] ([category_feature_id]),
	constraint [fk_product_feature_product] foreign key ([product_id]) references [product] ([product_id])
) ;

		create trigger [tr_product_feature0] 
		after update 
		of [product_feature_id], [category_feature_id], [value], [product_id] 
		on [product_feature] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [product_feature] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[product_feature_id]=[product_feature_id];
		end;
		;
create table [language] (
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[code] varchar(32),
	[short_code] varchar(5),
	[sid] integer,
	[langid] integer,
	[published] integer default (1),
	[backup_langid] integer null,
	constraint [pk_language] primary key ([langid]),
	constraint [language_unique0] unique ([code]),
	constraint [language_unique1] unique ([short_code]),
	constraint [language_unique2] unique ([code]),
	constraint [language_unique3] unique ([short_code]),
	constraint [fk_language_backup_language] foreign key ([backup_langid]) references [language] ([langid]),
	constraint [fk_language_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_language_backup_language] foreign key ([backup_langid]) references [language] ([langid]),
	constraint [fk_language_sidindex] foreign key ([sid]) references [sid_index] ([sid])
) ;

		create trigger [tr_language0] 
		after update 
		of [code], [short_code], [sid], [langid], [published], [backup_langid] 
		on [language] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [language] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[langid]=[langid];
		end;
		;
create table [category_feature_group] (
	[category_feature_group_id] integer,
	[feature_group_id] integer,
	[catid] integer,
	[no] integer null,
	constraint [pk_category_feature_group] primary key ([category_feature_group_id]),
	constraint [category_feature_group_unique0] unique ([catid], [feature_group_id]),
	constraint [category_feature_group_unique1] unique ([catid], [feature_group_id]),
	constraint [fk_category_feature_group_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_category_feature_group_feature_group] foreign key ([feature_group_id]) references [feature_group] ([feature_group_id]),
	constraint [fk_category_feature_group_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_category_feature_group_feature_group] foreign key ([feature_group_id]) references [feature_group] ([feature_group_id])
) ;
create table [sid_index] (
	[dummy] smallint null,
	[sid] integer primary key autoincrement
) ;
create table [product_series] (
	[supplier_id] integer,
	[catid] integer null,
	[series_id] integer,
	[family_id] integer,
	[sid] integer,
	[tid] integer,
	constraint [pk_product_series] primary key ([series_id]),
	constraint [fk_product_series_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_product_series_product_family] foreign key ([family_id]) references [product_family] ([family_id]),
	constraint [fk_product_series_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_product_series_supplier] foreign key ([supplier_id]) references [supplier] ([supplier_id]),
	constraint [fk_product_series_tidindex] foreign key ([tid]) references [tid_index] ([tid]),
	constraint [fk_product_series_category] foreign key ([catid]) references [category] ([catid]),
	constraint [fk_product_series_product_family] foreign key ([family_id]) references [product_family] ([family_id]),
	constraint [fk_product_series_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_product_series_supplier] foreign key ([supplier_id]) references [supplier] ([supplier_id]),
	constraint [fk_product_series_tidindex] foreign key ([tid]) references [tid_index] ([tid])
) ;
create table [category] (
	[thumb_pic] varchar(255) default ('') null,
	[watched_top10] integer default (0),
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[catid] integer,
	[searchable] integer default (0),
	[ssid] integer null,
	[low_pic] varchar(255) default (''),
	[visible] integer default (0),
	[pcatid] integer null,
	[sid] integer,
	[tid] integer,
	[ucatid] varchar(255) null,
	[last_published] integer default (0) null,
	constraint [pk_category] primary key ([catid]),
	constraint [ucatid] unique ([ucatid]),
	constraint [ucatid] unique ([ucatid]),
	constraint [fk_category_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_category_tidindex] foreign key ([tid]) references [tid_index] ([tid]),
	constraint [fk_category_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_category_tidindex] foreign key ([tid]) references [tid_index] ([tid])
) ;

		create trigger [tr_category0] 
		after update 
		of [thumb_pic], [watched_top10], [catid], [searchable], [ssid], [low_pic], [visible], [pcatid], [sid], [tid], [ucatid], [last_published] 
		on [category] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [category] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[catid]=[catid];
		end;
		;
create table [vocabulary] (
	[record_id] integer,
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[langid] integer default (0),
	[value] varchar(255) null,
	[sid] integer,
	constraint [pk_vocabulary] primary key ([record_id]),
	constraint [vocabulary_unique0] unique ([sid], [langid]),
	constraint [vocabulary_unique1] unique ([sid], [langid]),
	constraint [fk_vocabulary_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_vocabulary_sidindex] foreign key ([sid]) references [sid_index] ([sid]),
	constraint [fk_vocabulary_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_vocabulary_sidindex] foreign key ([sid]) references [sid_index] ([sid])
) ;

		create trigger [tr_vocabulary0] 
		after update 
		of [record_id], [langid], [value], [sid] 
		on [vocabulary] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [vocabulary] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[record_id]=[record_id];
		end;
		;
create table [product_description] (
	[product_description_id] integer primary key autoincrement,
	[manual_pdf_url] varchar(255) default (''),
	[updated] timestamp default (strftime('%Y-%m-%d %H:%M:%f', 'now')),
	[specs_url] varchar(512) default (''),
	[option_field_1] text null,
	[product_id] integer,
	[option_field_2] text null,
	[support_url] varchar(255) default (''),
	[pdf_url] varchar(255) default (''),
	[short_desc] varchar(3000) default (''),
	[langid] integer,
	[pdf_size] integer default (0) null,
	[manual_pdf_size] integer default (0) null,
	[long_desc] text,
	[manual_pdf_updated] integer default (0),
	[manual_pdf_url_origin] text null,
	[warranty_info] text null,
	[pdf_url_origin] text null,
	[pdf_updated] integer default (0),
	[official_url] text null,
	constraint [product_description_unique0] unique ([product_id], [langid]),
	constraint [product_description_unique1] unique ([product_id], [langid]),
	constraint [fk_product_description_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_description_language] foreign key ([langid]) references [language] ([langid]),
	constraint [fk_product_description_product] foreign key ([product_id]) references [product] ([product_id]),
	constraint [fk_product_description_language] foreign key ([langid]) references [language] ([langid])
) ;

		create trigger [tr_product_description0] 
		after update 
		of [product_description_id], [manual_pdf_url], [specs_url], [option_field_1], [product_id], [option_field_2], [support_url], [pdf_url], [short_desc], [langid], [pdf_size], [manual_pdf_size], [long_desc], [manual_pdf_updated], [manual_pdf_url_origin], [warranty_info], [pdf_url_origin], [pdf_updated], [official_url] 
		on [product_description] for each row 
--		when ([new].[updated]=[old].[updated])
		begin
			update [product_description] 
			set [updated]=strftime('%Y-%m-%d %H:%M:%f', 'now')
			where [new].[product_description_id]=[product_description_id];
		end;
		;

	PRAGMA foreign_keys = ON;
	;