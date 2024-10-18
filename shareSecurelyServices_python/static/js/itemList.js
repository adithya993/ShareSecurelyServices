function deleteItem(e){
    grpName = $($(e).parent().parent().find(".itemGroupName"))[0].innerText
    itemName = $($(e).parent().parent().find(".itemName"))[0].innerText
    $('#deleteItem_itemGroupName').val(grpName)
    $('#deleteItem_itemName').val(itemName)
    $('#deleteGroupItembutton').click()
}

function addFeedBack(e){
    grpName = $($(e).parent().parent().find(".itemGroupName"))[0].innerText
    itemName = $($(e).parent().parent().find(".itemName"))[0].innerText
    $('#submitFeedback_itemGroupName').val(grpName)
    $('#submitFeedback_itemName').val(itemName)
    $('#submitFeedbackGroupItembutton').click()
}

$('#uplodedItemsInThisGroup > tbody  > tr').each(function (i) {
    if(i > 0){
        var self = $(this);
        var itemOwner = self.find("td:eq(2)").text().trim();
        if(itemOwner != $('#currentuseremail').val()){
           $(this).find('.btn-deleteItem').addClass('delItem');
        }
    }    
});