CREATE TABLE 
	`mis_2023`.`web_case_study` (
		`id` INT(10) NOT NULL AUTO_INCREMENT , 
		`csAuthor` VARCHAR(255) NOT NULL , 
		`csPurpose` VARCHAR(255) NOT NULL , 
		`csIntro` VARCHAR(255) NOT NULL , 
		`csKeyMsg` VARCHAR(255) NOT NULL , 
		`csType` VARCHAR(255) NOT NULL , 
		`csTypeIntervention` VARCHAR(255) NOT NULL , 
		`csTypeInterventionDate` VARCHAR(255) NOT NULL , 
		`csTypeInterventionArea` VARCHAR(255) NOT NULL , 
		`csProductProducedTitle` VARCHAR(255) NOT NULL , 
		`csProductProducedType` VARCHAR(255) NOT NULL , 
		`csProductProducedDate` VARCHAR(255) NOT NULL , 
		`csProductProducedArea` VARCHAR(255) NOT NULL , 
		`cs_sit_prior_act_chnge` VARCHAR(255) NOT NULL , 
		`cs_part_change_rel_proj` VARCHAR(255) NOT NULL , 
		`cs_part_change_rel_proj_date_start` VARCHAR(255) NOT NULL , 
		`cs_part_change_rel_proj_date_end` VARCHAR(255) NOT NULL , 
		`cs_sit_aff_proj` VARCHAR(255) NOT NULL , 
		`cs_proj_achv_action` VARCHAR(255) NOT NULL , 
		`cs_change_realized` VARCHAR(255) NOT NULL , 
		`cs_change_realized_date` VARCHAR(255) NOT NULL , 
		`cs_unpl_pln_pos_neg` VARCHAR(255) NOT NULL , 
		`cs_tang_demo_chnge_taken` VARCHAR(255) NOT NULL , 
		`cs_key_chng_exp_ocour_not` VARCHAR(255) NOT NULL , 
		`cs_chngs_ocour` VARCHAR(255) NOT NULL , 
		`cs_sig_chng` VARCHAR(255) NOT NULL , 
		`cs_pot_lterm_imp` VARCHAR(255) NOT NULL , 
		`cs_ind_sust_chng_like` VARCHAR(255) NOT NULL , 
		`cs_key_fact_cnhge_happen` VARCHAR(255) NOT NULL , 
		`cs_analysis_attrib_proj` VARCHAR(255) NOT NULL , 
		`cs_ind_fact_ifl_chng` VARCHAR(255) NOT NULL , 
		`cs_chng_interv_design_imp` VARCHAR(255) NOT NULL , 
		`cs_lesson_org_sim_sect_work` VARCHAR(255) NOT NULL , 
		`cs_photo_act` VARCHAR(255) NOT NULL , 
		`cs_vid_media_links` VARCHAR(255) NOT NULL , 
		`cs_quotes` VARCHAR(255) NOT NULL , 
		`cs_quotes_ref` VARCHAR(255) NOT NULL , 
		`cs_quotes_designation` VARCHAR(255) NOT NULL , 
		`cs_quotes_date` VARCHAR(255) NOT NULL , 
		`cs_quotes_topic` VARCHAR(255) NOT NULL , 
		`date_created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , 
		`date_modified` TIMESTAMP on update CURRENT_TIMESTAMP NOT NULL , 
		PRIMARY KEY (`id`)
	) ENGINE = InnoDB;