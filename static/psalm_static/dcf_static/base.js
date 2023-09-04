
$(document).ready(function(){
$(".hidden-textbox").hide();
$("select#form_1_commodity,select#form_2_commodity,select#cbb_commodity,select#mgit_commodity,select#form_6_commodity,select#form_7_commodity,select#form_11_industry_cluster").change(function(){
var currentVal = $(this).val();
if(currentVal == "PFN"){
$(".hidden-textbox").show();
}
else
$(".hidden-textbox").hide();
});  
});

$(document).ready(function(){
  $(".hidden-textbox2").hide();
  $("select#form_11_dip_alignment").change(function(){
  var currentVal = $(this).val();
  if(currentVal == "Yes"){
  $(".hidden-textbox2").show();
  }
  else
  $(".hidden-textbox2").hide();
  });  
  });

  $(document).ready(function(){
    $(".hidden-textbox2").hide();
    
    $("select#form_2_remarks_status").change(function(){
        var currentVal = $(this).val();
        var hiddenTextbox = $(".hidden-textbox2");
        
        if (currentVal == "Cancelled" || currentVal == "Non-renewal") {
            hiddenTextbox.show();
            hiddenTextbox.prop("required", true); 
        } else {
            hiddenTextbox.hide();
            hiddenTextbox.prop("required", false);
        }
    });  
});

$(document).ready(function() {
  $(".form-1-y, .form-1-ac, .form-1-ad, .form-1-ae").on("input", updateTotalProjectCost);

  function updateTotalProjectCost() {
      const yValue = parseFloat($(this).closest("tr").find(".form-1-y").val()) || 0;
      const acValue = parseFloat($(this).closest("tr").find(".form-1-ac").val()) || 0;
      const adValue = parseFloat($(this).closest("tr").find(".form-1-ad").val()) || 0;
      const aeValue = parseFloat($(this).closest("tr").find(".form-1-ae").val()) || 0;
      const totalProjectCost = yValue + acValue + adValue + aeValue;
      $(this).closest("tr").find(".form-1-totalproject_cost").val(totalProjectCost);
  }
});

$(document).ready(function() {
  $(".form_1_euqipments, .form_1_Facilities_warehouses").on("input", updateTotalProdInv);

  function updateTotalProdInv() {
      const form_1_euqipments2 = parseFloat($(this).closest("tr").find(".form_1_euqipments").val()) || 0;
      const form_1_Facilities_warehouses2 = parseFloat($(this).closest("tr").find(".form_1_Facilities_warehouses").val()) || 0;
      const totalProdInv = form_1_euqipments2 + form_1_Facilities_warehouses2;
      $(this).closest("tr").find(".form_1_total_prod_invs").val(totalProdInv);
      $("#form_1_totalcost_prodinvest2").val(totalProdInv);
      $("#form_1_totalcost_prodinvest3").val(totalProdInv);
      $(".form_1_totalcost_prodinvest3").val(totalProdInv);

  }
});

function updateTimestamps() {
  $('.date-cell').each(function() {
    const timestamp = new Date($(this).data('timestamp'));
    const now = new Date();

    const diffInSeconds = Math.floor((now - timestamp) / 1000);

    if (diffInSeconds < 60) {
      $(this).text(`${diffInSeconds} seconds ago`);
    } else if (diffInSeconds < 3600) {
      const diffInMinutes = Math.floor(diffInSeconds / 60);
      $(this).text(`${diffInMinutes} minutes ago`);
    } else if (diffInSeconds < 86400) {
      const diffInHours = Math.floor(diffInSeconds / 3600);
      $(this).text(`${diffInHours} hours ago`);
    } else {
      // Display the full date
      const formattedDate = `${timestamp.toLocaleDateString()} ${timestamp.toLocaleTimeString()}`;
      $(this).text(formattedDate);
    }
  });
}

updateTimestamps();

$(document).ready(function() {
  $(".form-1-aa").on("input", updateTotalMatchingGrant);
  $(".form-1-ab").on("input", updateTotalMatchingGrant);
  $("#form_1_totalcost_prodinvest2").on("input", updateTotalMatchingGrant);
  

  function updateTotalMatchingGrant() {
      const aaValue = parseFloat($(this).closest("tr").find(".form-1-aa").val()) || 0;
      const abValue = parseFloat($(this).closest("tr").find(".form-1-ab").val()) || 0;
      const acValue = parseFloat($(this).closest("tr").find("#form_1_totalcost_prodinvest2").val()) || 0;
      const total = $(this).closest("tr").find(".form-1-total-matching-grant-update");
      const totalMatchingGrant = aaValue + abValue + acValue;
      total.val(totalMatchingGrant);
  }
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
$(".hidden-textbox2").hide();
$("select#industry_cluster").change(function(){
var currentVal = $(this).val();
if(currentVal == ""){
$(".hidden-textbox2").show();
}
else
$(".hidden-textbox2").hide();
});  
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
$(".hidden-textbox3").hide();
$("select#no_indigenous_group").change(function(){
var currentVal = $(this).val();
if(currentVal == "Yes"){
$(".hidden-textbox3").show();
}
else
$(".hidden-textbox3").hide();
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

$(document).ready(function(){
  var multipleCancelButton = new Choices('#form_3_choices_multiple_remove_button', {
    removeItemButton: true,
    maxItemCount:4,
    searchResultLimit:4,
    renderChoiceLimit:4
  }); 
});






function toastr(type, message, title, options) {
  toastr.options = options;
  toastr[type](message, title);
}
 