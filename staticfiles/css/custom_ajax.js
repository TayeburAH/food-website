function call_ajax( $cart ,formData,url){
		$.ajax({
				   url:url,
				   type:'get',
				   data:formData,

				   success:function (data) {

				   console.log(data.status);
				   $cart.parents('.Quantity').siblings('.Subtotal').text("$ " + data.sub_total);

				   $cart.parent().children().eq(1).val(data.quantity);

					},

				   error:function (error) {
				   console.log(error)
				   }
		});