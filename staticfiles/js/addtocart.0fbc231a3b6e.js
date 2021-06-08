
$(document).ready(function(){

  // jQuery methods/events go here...

            // Display the price of the one checked
            // Get the price on click, change function

            $(".form-check-input").change(function () {
            var show_price = $(this).val();
            $(this).parents('.form-group').siblings('.row').find('.show-price').html(`<strong>$ ${show_price}</strong>`);
            });



            $(".product-form").submit(function(e){
            e.preventDefault();      // Prevent default
            var $form = $(this);    //Do $form and $form.find('') this when you have many forms with many identical form

            var product_id = $form.find("#product-id").val();
            var price = $form.find(".form-check-input:checked").val();
            var size = $form.find(".form-check-input:checked").attr('data-size-type');
            console.log(product_id,price,size);

            if( user == 'AnonymousUser'){
            alert('You need to create an account');
            // will stop here if its true
            }else if( size == undefined){
            alert('You did not select size');
            // will stop here if its true
            }else{
           // Will come here if non of them are true
            var formData = {
              "product_id" : product_id,
              "price" : price,
              "size" : size,
              "operation":'add_to_cart',
            };

             var url = "/cart_operation/"   // The view name which will process the data
              $.ajax({
                       url:url,
                       type:'get',
                       data:formData,

                        beforeSend: function() {
                            $('.semi-transparent').animate({
                                opacity: 0.5,
                              });
                            $('#loader').fadeIn().removeClass('hidden');
                        },

                       success:function (data) {
                       console.log(data.status);
                       console.log(data.Quantity);

                       $('#cart').find('span').text(data.Quantity);

                       if (data.limit == 'True' ){
                       alert('You can only order maximum of 5');
                       }
                       },

                        //Stop when completed
                        complete: function(){
                        $('.semi-transparent').animate({
                            opacity: 1,
                          });
                        $('#loader').fadeOut().addClass('hidden');
                        },

                       error:function (error) {
                       console.log(error)
                       }



                });
                }
        });


});











