let CHOICES_SELECT = {}





$(document).ready(function(){
	$(".hidden-form11").hide();
	$("select#form_11_dip_alignment").change(function(){
	var currentVal = $(this).val();
	if(currentVal == "Yes"){
	$(".hidden-form11").show();
	}
	else
	$(".hidden-form11").hide();
	});  
	});

	$(document).ready(function(){
		$(".hidden-textboxform9").hide();
		$("select#form_9_type_of_training").change(function(){
		var currentVal = $(this).val();
		if(currentVal == "other"){
		$(".hidden-textboxform9").show();
		}
		else
		$(".hidden-textboxform9").hide();
		});  
		});

		$(document).ready(function(){
			$(".hidden-textboxform6").hide();
			$("select#form_6_commodity1").change(function(){
			var currentVal = $(this).val();
			if(currentVal == "other"){
			$(".hidden-textboxform6").show();
			}
			else
			$(".hidden-textboxform6").hide();
			});  
			});

			$(document).ready(function(){
				$(".hidden-textboxform62").hide();
				$("select#form_6_commodity2").change(function(){
				var currentVal = $(this).val();
				if(currentVal == "other"){
				$(".hidden-textboxform62").show();
				}
				else
				$(".hidden-textboxform62").hide();
				});  
				});
	




$(document).ready(function() {
	$(".form1_mg, .form1_cap, .form1_sup").on("input", updateTotalProjectCost);

	function updateTotalProjectCost() {
			const form1_mgz = parseFloat($(this).closest("tr").find(".form1_mg").val()) || 0;
			const form1_capz = parseFloat($(this).closest("tr").find(".form1_cap").val()) || 0;
			const form1_supz = parseFloat($(this).closest("tr").find(".form1_sup").val()) || 0;
			const totalProjectCost = form1_mgz + form1_capz + form1_supz;
			$(this).closest("tr").find(".form-1-totalproject_cost").val(totalProjectCost);
	}
});

    function calculateTotaltable() {
        const largeEnterprise = parseInt($('#total_large_enterprise').val()) || 0;
        const mediumEnterprise = parseInt($('#total_medium_enterprise').val()) || 0;
        const smallEnterprise = parseInt($('#total_small_enterprise').val()) || 0;
        const microEnterprise = parseInt($('#total_micro_enterprise').val()) || 0;
		const totalMale = parseInt($('#form_1_totalmale').val()) || 0;
        const totalFemale = parseInt($('#form_1_totalfemale').val()) || 0;
        const maleYouth = parseInt($('#form_1_maleyouth').val()) || 0;
        const femaleYouth = parseInt($('#form_1_femaleyouth').val()) || 0;
		const maleIp = parseInt($('#form_1_maleip').val()) || 0;
        const femaleIp = parseInt($('#form_1_femaleip').val()) || 0;
		const malePwd = parseInt($('#form_1_malepwd').val()) || 0;
        const femalePwd = parseInt($('#form_1_femalepwd').val()) || 0;
		const totalcoop = parseInt($('#form_1_totalcooperatives').val()) || 0;
        const totalassoc = parseInt($('#form_1_totalassociations').val()) || 0;
		const hectrehab = parseInt($('#form_1_hect_rehab').val()) || 0;
		const hectexp = parseInt($('#form_1_hect_exp').val()) || 0;
		const partcounter = parseInt($('#form_1_partners_counterpart').val()) || 0;
		const totalproj = parseInt($('#form_1_total_matching_grant').val()) || 0;
		const partcounterMG = parseInt($('#form_1_partners_counterpart').val()) || 0;
		const partcounterCB = parseInt($('#form_1_total_capbuild_counterpart').val()) || 0;
		const partcounterFMI = parseInt($('#fmi_part_counter').val()) || 0;
		const projcostMG = parseInt($('#form_1_y').val()) || 0;
		const projcostCB = parseInt($('#form_1_ac').val()) || 0;
		const projcostSCM = parseInt($('#form_1_ad').val()) || 0;
		const projcostFMI = parseInt($('#form_1_fmi').val()) || 0;
		const cbbmaleyouth = parseInt($('#cbb_male_youth').val()) || 0;
		const cbb_male_pwd = parseInt($('#cbb_male_pwd').val()) || 0;
		const cbb_male_sc = parseInt($('#cbb_male_sc').val()) || 0;
		const cbb_male_ip = parseInt($('#cbb_male_ip').val()) || 0;
		const cbbfemaleyouth = parseInt($('#cbb_female_youth').val()) || 0;
		const cbb_female_pwd = parseInt($('#cbb_female_pwd').val()) || 0;
		const cbb_female_sc = parseInt($('#cbb_female_sc').val()) || 0;
		const cbb_female_ip = parseInt($('#cbb_female_ip').val()) || 0;
		const counterpartscm = parseInt($('#supply_chain_manager_counterpart').val()) || 0;
		






        const total = largeEnterprise + mediumEnterprise + smallEnterprise + microEnterprise;
        const totalFarmerBene = totalMale + totalFemale;
		const totalYouth = maleYouth + femaleYouth;
		const totalIp = maleIp + femaleIp;
		const totalPwd = malePwd + femalePwd;
		const totalfo = totalcoop + totalassoc;
		const hectcovered = hectrehab + hectexp;
		const mgcost = partcounter + totalproj;
		const partcounterTotal = partcounterMG + partcounterCB + counterpartscm + partcounterFMI;
		const dipcostMG = partcounterMG + projcostMG;
		const dipcostCB = partcounterCB + projcostCB;
		const dipcostSCM = counterpartscm + projcostSCM;
		const dipcostFMI = partcounterFMI + projcostFMI;
		const totaldip = dipcostMG + dipcostCB + dipcostSCM + dipcostFMI;
		const totalcbbmale = cbbmaleyouth + cbb_male_pwd + cbb_male_sc + cbb_male_ip;
		const totalcbbfemale = cbbfemaleyouth + cbb_female_pwd + cbb_female_sc + cbb_female_ip;
		const totalcounterpartcb = partcounterCB;
		const totalcounterpartmg = partcounterMG;
		const totalcounterpartscm =counterpartscm;
		const totalprojcostfmi = projcostFMI;
		const totalcounterpartfmi=partcounterFMI;




        $('#form_1_totalmsme').val(total);
        $('#form_1_total_farmerbene').val(totalFarmerBene);
		$('#form_1_totalyouth').val(totalYouth);
        $('#form_1_totalip').val(totalIp);
        $('#form_1_totalpwd').val(totalPwd);
        $('#form_1_totalfo').val(totalfo);
        $('#form_1_totalhectarage_cov').val(hectcovered);
        $('#form1_total_mg_cost').val(mgcost);
        $('#partner_counterpart_total').val(partcounterTotal);

		$('#total_dip_cost_MG').val(dipcostMG);
        $('#total_dip_cost_CB').val(dipcostCB);
        $('#total_dip_cost_SCM').val(dipcostSCM);
        $('#total_dip_cost_FMI').val(dipcostFMI);
        $('#total_dip_cost_total').val(totaldip);

        $('#cbb_male_total').val(totalcbbmale);
        $('#cbb_female_total').val(totalcbbfemale);
		$('#partner_counterpart_CB').val(totalcounterpartcb);
		$('#partner_counterpart_MG').val(totalcounterpartmg);
		$('#partner_counterpart_SCM').val(totalcounterpartscm);
		$('#form1_total_fmi').val(totalprojcostfmi);
		$('#partner_counterpart_FMI').val(totalcounterpartfmi);






   









    }

    $('#total_large_enterprise, #total_medium_enterprise, #total_small_enterprise, #total_micro_enterprise,#form_1_totalmale, #form_1_totalfemale,#form_1_maleyouth, #form_1_femaleyouth,#form_1_maleip, #form_1_femaleip,#form_1_malepwd, #form_1_femalepwd,#form_1_totalcooperatives,#form_1_totalassociations,#form_1_hect_rehab,#form_1_hect_exp,#form_1_partners_counterpart,#form_1_total_matching_grant,#partner_counterpart_MG,#partner_counterpart_CB,#partner_counterpart_SCM,#partner_counterpart_FMI,#form_1_y,#form_1_ac,#form_1_ad,#form1_total_fmi,#cbb_male_youth,#cbb_male_pwd,#cbb_male_sc,#cbb_male_ip,#cbb_female_youth,#cbb_female_pwd,#cbb_female_sc,#cbb_female_ip,#form_1_total_capbuild_counterpart,#supply_chain_manager_counterpart,#form_1_fmi,#fmi_part_counter').on('input', calculateTotaltable);

    calculateTotaltable();



document.addEventListener('DOMContentLoaded', function () {
  // Function for updating total production investment
  function updateTotalProdInv() {
    const form1Equipments = parseFloat(this.closest('tr').querySelector('.form_1_euqipments').value) || 0;
    const form1FacilitiesWarehouses = parseFloat(this.closest('tr').querySelector('.form_1_Facilities_warehouses').value) || 0;
    const totalProdInv = form1Equipments + form1FacilitiesWarehouses;
    this.closest('tr').querySelector('.form_1_total_prod_invs').value = totalProdInv;
    document.getElementById('form_1_totalcost_prodinvest2').value = totalProdInv;
    document.getElementById('form_1_totalcost_prodinvest3').value = totalProdInv;
    document.querySelector('.form_1_totalcost_prodinvest3').value = totalProdInv;
  }

  // Event listener for form_1_euqipments and form_1_Facilities_warehouses
  document.querySelectorAll('.form_1_euqipments, .form_1_Facilities_warehouses').forEach(function (element) {
    element.addEventListener('input', updateTotalProdInv);
  });

  // Function for updating total capital
  function updateTotalCap() {
    const form1Org = parseFloat(this.closest('tr').querySelector('.form1_org').value) || 0;
    const form1Tech = parseFloat(this.closest('tr').querySelector('.form1_tech').value) || 0;
    const form1PostProd = parseFloat(this.closest('tr').querySelector('.form1_postprod').value) || 0;
    const form1Other = parseFloat(this.closest('tr').querySelector('.form1_otherz').value) || 0;
    const totalCap = form1Org + form1Tech + form1PostProd + form1Other;
    this.closest('tr').querySelector('.form1_total_caps').value = totalCap;
    document.querySelector('.form1_cap').value = totalCap;
  }

  // Event listener for form1_org, form1_tech, form1_postprod, and form1_otherz
  document.querySelectorAll('.form1_org, .form1_tech, .form1_postprod, .form1_otherz').forEach(function (element) {
    element.addEventListener('input', updateTotalCap);
  });

  // Event listener for form_1_supply_chain_manager
document.addEventListener('DOMContentLoaded', function () {
  var supplyChainManagerInput = document.getElementById('form_1_supply_chain_manager');

  if (supplyChainManagerInput) {
    supplyChainManagerInput.addEventListener('input', function () {
      var supplyChainManagerValue = this.value;
      document.querySelector('.form1_sup').value = supplyChainManagerValue;
    });
  }
});
  // Function for updating total matching grant
  function updateTotalMatchingGrant() {
    const aaValue = parseFloat(this.closest('tr').querySelector('.form-1-aa').value) || 0;
    const abValue = parseFloat(this.closest('tr').querySelector('.form-1-ab').value) || 0;
    const acValue = parseFloat(document.getElementById('form_1_totalcost_prodinvest2').value) || 0;
    const totalMatchingGrant = aaValue + abValue + acValue;
    this.closest('tr').querySelector('.form-1-total-matching-grant-update').value = totalMatchingGrant;
    document.querySelector('.form1_mg').value = totalMatchingGrant;
  }

  // Event listeners for form-1-aa, form-1-ab, and form_1_totalcost_prodinvest2
  document.querySelectorAll('.form-1-aa, .form-1-ab, #form_1_totalcost_prodinvest2').forEach(function (element) {
    element.addEventListener('input', updateTotalMatchingGrant);
  });
});


$(document).ready(function() {
	$(".form-1-aa2").on("input", updateTotalMatchingGrant);
	$(".form-1-ab2").on("input", updateTotalMatchingGrant);
	$(".form_1_totalcost_prodinvest3").on("input", updateTotalMatchingGrant);
	

	function updateTotalMatchingGrant() {
			const aaValue2 = parseFloat($(this).closest("tr").find(".form-1-aa2").val()) || 0;
			const abValue2 = parseFloat($(this).closest("tr").find(".form-1-ab2").val()) || 0;
			const acdalue2 = parseFloat($(this).closest("tr").find(".form_1_totalcost_prodinvest3").val()) || 0;
			const total2 = $(this).closest("tr").find(".form-1-total-matching-grant-update2");
			const totalMatchingGrant2 = aaValue2 + abValue2 + acdalue2;
			total2.val(totalMatchingGrant2);
	}
});



$(document).ready(function(){
$(".hidden-column_18_21").hide();
$("select#type_assistance").change(function(){
var currentVal = $(this).val();
if(currentVal == "product_dev"){
$(".hidden-column_18_21").show();
}
else
$(".hidden-column_18_21").hide();
});  
});


$(document).ready(function(){
$(".hidden-column_9_18").hide();
$("select#type_inv_match").change(function(){
var currentVal = $(this).val();
if(currentVal == "expansion" || currentVal == "productive_investment"){
$(".hidden-column_9_18").show();
}
else
$(".hidden-column_9_18").hide();
});  
});

$(document).ready(function(){
$(".hidden-column_19_26").hide();
$("select#type_inv_match").change(function(){
var currentVal = $(this).val();
if(currentVal == "rehabilitation"){
$(".hidden-column_19_26").show();
}
else
$(".hidden-column_19_26").hide();
});  
});

$(document).ready(function(){
$(".hidden-column_22_28").hide();
$("select#type_assistance").change(function(){
var currentVal = $(this).val();
if(currentVal == "consultancy_serv"){
$(".hidden-column_22_28").show();
}
else
$(".hidden-column_22_28").hide();
});  
});





$(document).ready(function(){
$(".hidden-textbox4").hide();
$("select#form_interprise2").change(function(){
var currentVal = $(this).val();
if(currentVal == "Yes"){
$(".hidden-textbox4").show();
}
else
$(".hidden-textbox4").hide();
});  
});

$(document).ready(function(){
$(".hidden-textbox5").hide();
$("select#pricing").change(function(){
var currentVal = $(this).val();
if(currentVal == "Yes"){
$(".hidden-textbox5").show();
}
else
$(".hidden-textbox5").hide();
});  
});

$(document).ready(function(){
$(".hidden-textbox6").hide();
$("select#quality_raw").change(function(){
var currentVal = $(this).val();
if(currentVal == "Yes"){
$(".hidden-textbox6").show();
}
else
$(".hidden-textbox6").hide();
});  
});

$(document).ready(function(){
$(".hidden-textbox7").hide();
$("select#quality_final_prod").change(function(){
var currentVal = $(this).val();
if(currentVal == "Yes"){
$(".hidden-textbox7").show();
}
else
$(".hidden-textbox7").hide();
});  
});

$(document).ready(function(){
$(".hidden-textbox8").hide();
$("select#existing_comm").change(function(){
var currentVal = $(this).val();
if(currentVal == "Yes"){
$(".hidden-textbox8").show();
}
else
$(".hidden-textbox8").hide();
});  
});

$(document).ready(function(){
$(".hidden-textbox9").hide();
$("select#prov_supp_assis").change(function(){
var currentVal = $(this).val();
if(currentVal == "Yes"){
$(".hidden-textbox9").show();
}
else
$(".hidden-textbox9").hide();
});  
});

$(document).ready(function(){
$(".hidden-textbox10").hide();
$("select#business_prodc3").change(function(){
var currentVal = $(this).val();
if(currentVal == "Yes"){
$(".hidden-textbox10").show();
}
else
$(".hidden-textbox10").hide();
});  
});
$(document).ready(function(){
$(".hidden-textbox11").hide();
$("select#member_following").change(function(){
var currentVal = $(this).val();
if(currentVal == "orgs"){
$(".hidden-textbox11").show();
}
else
$(".hidden-textbox11").hide();
});  
});

$(document).ready(function(){
$(".hidden-textbox12").hide();
$("select#member_livelihood").change(function(){
var currentVal = $(this).val();
if(currentVal == "Yes"){
$(".hidden-textbox12").show();
}
else
$(".hidden-textbox12").hide();
});  
});

$(document).ready(function(){
$(".hidden-textbox13").hide();
$("select#dip_alignment_prod").change(function(){
var currentVal = $(this).val();
if(currentVal == "dipyesprod"){
$(".hidden-textbox13").show();
}
else
$(".hidden-textbox13").hide();
});  
});


$(document).ready(function(){
$(".hidden-textbox14").hide();
$("select#dip_alignment").change(function(){
var currentVal = $(this).val();
if(currentVal == "dipyes"){
$(".hidden-textbox14").show();
}
else
$(".hidden-textbox14").hide();
});  
});

$(document).ready(function(){
$(".hidden-textbox15").hide();
$("select#title_cert").change(function(){
var currentVal = $(this).val();
if(currentVal == "other_specifics"){
$(".hidden-textbox15").show();
}
else
$(".hidden-textbox15").hide();
});  
});

$(document).ready(function(){
		$(".hidden-textbox17").hide();
		$("select#training_act_en").change(function(){
		var currentVal = $(this).val();
		if(currentVal == "training_act_spec"){
		$(".hidden-textbox17").show();
		}
		else
		$(".hidden-textbox17").hide();
		});  
		});

 
$(document).ready(function(){
$(".hidden-textbox16").hide();
$("select#title_cert2").change(function(){
var currentVal = $(this).val();
if(currentVal == "others_specifics"){
$(".hidden-textbox16").show();
}
else
$(".hidden-textbox16").hide();
});  
});


$(document).ready(function(){
		$(".hidden-textbox19").hide();
		$("select#industry_clus_eq").change(function(){
		var currentVal = $(this).val();
		if(currentVal == "specsss"){
		$(".hidden-textbox19").show();
		}
		else
		$(".hidden-textbox19").hide();
		});  
		});



	 


function myFunction() {
var checkbox1 = document.getElementById("business_reg_check");
var checkbox2 = document.getElementById("product_reg_check");
var checkbox3 = document.getElementById("cert_reg");
var checkbox4 = document.getElementById("lic_op");
var checkbox5 = document.getElementById("iso_cert");
var checkbox6 = document.getElementById("gapgmp_cert");
var checkbox7 = document.getElementById("organic");
var checkbox8 = document.getElementById("halal");
var checkbox9 = document.getElementById("other_cert");
var checkbox10 = document.getElementById("others_specific_products_checkbox");
var textt = document.getElementById("textt");
var textt2 = document.getElementById("textt2");
var textt3 = document.getElementById("textt3");
var textt4 = document.getElementById("textt4");
var textt5= document.getElementById("textt5");
var textt6 = document.getElementById("textt6");
var textt7 = document.getElementById("textt7");
var textt8 = document.getElementById("textt8");
var textt9 = document.getElementById("textt9");
var textt10 = document.getElementById("textt10");

if (checkbox1.checked == true){
textt.style.display = "block";
} else{
textt.style.display = "none";
}
if (checkbox2.checked == true){
textt2.style.display = "block";
} else {
textt2.style.display = "none";
}

if (checkbox3.checked == true){
textt3.style.display = "block";
} else {
textt3.style.display = "none";
}

if (checkbox4.checked == true){
textt4.style.display = "block";
} else {
textt4.style.display = "none";
}

if (checkbox5.checked == true){
textt5.style.display = "block";
} else{
textt5.style.display = "none";
}

if (checkbox5.checked == true){
iso_cert_specific.style.display = "block";
} else{
iso_cert_specific.style.display = "none";
}

if (checkbox6.checked == true){
textt6.style.display = "block";
} else {
textt6.style.display = "none";
}

if (checkbox6.checked == true){
textt6.style.display = "block";
} else {
textt6.style.display = "none";
}

if (checkbox7.checked == true){
textt7.style.display = "block";
} else {
textt7.style.display = "none";
}

if (checkbox8.checked == true){
textt8.style.display = "block";
} else {
textt8.style.display = "none";
}

if (checkbox9.checked == true){
textt9.style.display = "block";
} else {
textt9.style.display = "none";
}
if (checkbox9.checked == true){
other_cert_specify.style.display = "block";
} else {
other_cert_specify.style.display = "none";
}

if (checkbox10.checked == true){
others_specific_products.style.display = "block";
} else{
others_specific_products.style.display = "none";
}







}
function myFunction2() {

var checkbox11 = document.getElementById("other_orgs_checkbox");

if (checkbox11.checked == true){
		other_orgs_pls_spec.style.display = "block";
} else{
				other_orgs_pls_spec.style.display = "none";
}

}

function myFunction3() {

		var checkbox12 = document.getElementById("other_orgs_checkbox");
		
		if (checkbox12.checked == true){
				other_orgs_pls_spec.style.display = "block";
		} else{
						other_orgs_pls_spec.style.display = "none";
		}
		
		}

		function calculateTotal() {
			var cash_sales = parseInt(document.getElementById('form_7_cash_sales').value) || 0;
			var booked_sales = parseInt(document.getElementById('form_7_booked_sales').value) || 0;
			var under_negotiations = parseInt(document.getElementById('form_7_under_negotiations').value) || 0;
			var total = cash_sales + booked_sales + under_negotiations;
			document.getElementById('form_7_total_autosum').value = total;
		}

		$(document).on("change","#filter1",(elem)=>{
				for (let count = 0; count < $(".filter2_opt").length; count++) { $(".filter2_opt")[count].style.display = "block"}
				$("#"+elem.target.value)[0].style.display = "none"
		})


		$('#chooseFile').bind('change', function () {
				var filename = $("#chooseFile").val();
				if (/^\s*$/.test(filename)) {
					$(".file-upload").removeClass('active');
					$("#noFile").text("No file chosen..."); 
				}
				else {
					$(".file-upload").addClass('active');
					$("#noFile").text(filename.replace("C:\\fakepath\\", "")); 
				}
			});
			
		
			function confirmation(e) {
				e.preventDefault();
		
				var url = e.currentTarget.getAttribute('href')

				Swal.fire({
					icon: 'warning',
					title: 'Are you sure you want to Delete this Data?',
					text: 'Deleting this data will permanently remove it from the database.',
					showCancelButton: true,
					confirmButtonColor: '#3085d6',
					cancelButtonColor: '#d33',
					confirmButtonText: 'Yes, delete!'
			}).then((result) => {
					if (result.value) {
							window.location.href=url;
					}
					
			})
		}


		var NavWithChild = (function() {

			// Variables

			var $nav = $('.nav-item.nav-with-child');
			setTimeout(function(){
				$nav.each(function(index, each) {

						$(each).on('click',function(event) {
							if($(each).is('.nav-item-expanded')) {
								$(each).removeClass('nav-item-expanded')

							} else {
									$(each).addClass('nav-item-expanded')
							}
						})
					});
			},300)



})();


$onload(function(){
		$('#datatable-responsive').dataTable({
		/* Disable initial sort */
		"aaSorting": []
		});
})

function toastr(type, message, title, options) {
	toastr.options = options;
	toastr[type](message, title);
}











 