/**
* Created by gdelnegro on 17/1/16.
*/
var method = undefined;

document.onreadystatechange = function () {
    if (document.readyState === "complete") {
        if (document.URL.indexOf("add") > -1){
            jQuery("#id_auxiliary_tag").val("");
            method = "add";
        }else if(document.URL.indexOf("change") > -1){
            method = "edit";
        }
        jQuery('#id_has_auxiliary_text').change(function() {
            if(jQuery(this).is(":checked")) {
                showFields();
            }else{
                hideFields();
            }
        });
    }
};

/**
* show/hide fields
*/
function showFields(){
    jQuery(".field-auxiliary_tag").val("");
    jQuery(".field-auxiliary_tag").show();
    jQuery('[class*=" field-auxiliary_tag"]').show();
}

function hideFields(){
    jQuery(".field-auxiliary_tag").val("");
    jQuery(".field-auxiliary_tag").hide();
    jQuery('[class*=" field-auxiliary_tag"]').hide();
}
