function grptables(e,val) {
    if (val == "req"){
        $(e).css("color","#ff7010");
        $(e).next().css("color","white");
        $('#viewMyGroups').hide();$('#viewRequestInMyGroups').show();
    }
    if (val == "view"){
        $(e).css("color","#ff7010");
        $(e).prev().css("color","white");
        $('#viewMyGroups').show();$('#viewRequestInMyGroups').hide();
    }

}

function myGroupGrant(e,val) {
    grpName = $($(e).parent().parent().find(".grpName"))[0].innerText
    requestedBy = $($(e).parent().parent().find(".reqby"))[0].innerText
    actionClicked = ""
    if(val == "Accept") {
        actionClicked = "Accept"
    }
    if(val == "Revoke") {
        actionClicked = "Revoke"
    }
    if(val == "Reject") {
        actionClicked = "Reject"
    }

    $('#grantgroupaccess_grpname').val(grpName)
    $('#grantgroupaccess_useremail').val(requestedBy)
    $('#grantgroupaccess_action').val(actionClicked)
    $('#grantgroupaccessbutton').click()
}

function selectedGroup(e, val) {
    grpName = $($(e).parent().parent().find(".grpName"))[0].innerText
    grpDesc = $($(e).parent().parent().find(".grpDesc"))[0].innerText
    grpOwner = $($(e).parent().parent().find(".grpOwner"))[0].innerText
    $('#selectedgroup_grpname').val(grpName)
    $('#selectedgroup_owner').val(grpOwner)
    $('#selectedgroupbutton').click()
}

$("#create_grpname").on({
    keydown: function(e) {
      if (e.which === 32)
        return false;
    },
    change: function() {
      this.value = this.value.replace(/\s/g, "");
    }
  });

 $('#viewUsersInMyGroups > tbody  > tr').each(function (i) {
    if(i > 0){
        var self = $(this);
        var itemOwner = self.find("td:eq(2)").text().trim();
        if(itemOwner == '1'){
           $($(this).find('.revokeFromGroup')).show();
           $($(this).find('.addToGroup')).hide();
           $($(this).find('.rejectRequest')).hide();
        } else {
            $($(this).find('.revokeFromGroup')).hide();
            $($(this).find('.addToGroup')).show();
            $($(this).find('.rejectRequest')).show();
        }
    }    
});