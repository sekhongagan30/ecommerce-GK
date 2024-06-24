console.log("new js")
const monthNames = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];


$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response){
            console.log("comment saved to db");
            if(response.bool==true){
                $("#review-resp").html("Review added successfully.")
                $(".hide-comment-form").hide()
                $(".add-review").hide()
                let _starString = ""
                for(var i=1; i<=response.context.rating; i++){
                _starString += `
                                <i class="fas fa-star text-warning"></i>
                `
                }
                let _html = `
                <div class="single-comment justify-content-between d-flex mb-30">
                    <div class="user justify-content-between d-flex">
                        <div class="thumb text-center">
                            <img src="/static/assets/imgs/blog/user.png" alt="" />
                            <a href="#" class="font-heading text-brand">${response.context.user}</a>
                        </div>
                        <div class="desc">
                            <div class="d-flex justify-content-between mb-10">
                                <div class="d-flex align-items-center">
                                    <span class="font-xs text-muted">${time}</span>
                                </div>
                                ${_starString}
                            </div>

                            <p class="mb-10">${response.context.review}</p>
                        </div>
                    </div>
                </div>
                `
                $(".comment-list").prepend(_html)
            }
            else{
                $("#review-resp").html("You need to be logged in to add a review !")
            }
        }
    })
})

$(document).ready(function(){
    $(".loader").hide()
    $(".filter-checkbox").on("click", function(){
        let filter_object = {}
        priceRangeFrom = $("#slider-range-value1").text()
        priceRangeTo = $("#slider-range-value2").text()
        priceRangeFrom = priceRangeFrom.replace("₹", "").replace(",", "")
        priceRangeTo= priceRangeTo.replace("₹", "").replace(",", "")
        filter_object['priceRangeFrom'] = priceRangeFrom
        filter_object['priceRangeTo'] = priceRangeTo
        console.log("product 87", filter_object)

        $(".filter-checkbox").each(function(index){ //each is basically for loop, which iterates thru all inputs with class filter-checkbox
            let filter_value = $(this).val() // value of checkbox input
                let filter_key = $(this).data("filter") // data-filter in checkbox input
            console.log(filter_value, filter_key);
            filter_object[filter_key] =
            Array.from(document.querySelectorAll('input[data-filter='+filter_key+']:checked')).map(function // this checks k jehra checkbox checked hai, usko map kia hai fn se,
            (element){
            return element.value // this fn will return value of input field
            })
        })
        $.ajax({
            url: '/filter-products', // here this url will be send to browser url
            data: filter_object,
            method: 'GET',
            dataType: 'json',
            beforeSend: function(){
                $(".loader").show()
            },
            success: function(res){
                console.log(res);
                $(".loader").show();
                $("#filtered-products").html(res.data);
                $(".numberOfProductsWhileFilter").html(res.totalProductsAfterFilter);
            }
        })
        console.log(filter_object); // {'category': ['1','3'], 'vendor': ['2']}
    })
    $(".priceRangeFilter").on("click", function(){
        let filter_object = {}
        priceRangeFrom = $("#slider-range-value1").text()
        priceRangeTo = $("#slider-range-value2").text()
        priceRangeFrom = priceRangeFrom.replace("₹", "").replace(",", "")
        priceRangeTo= priceRangeTo.replace("₹", "").replace(",", "")
        filter_object['priceRangeFrom'] = priceRangeFrom
        filter_object['priceRangeTo'] = priceRangeTo
        console.log("product 87", filter_object)

        $(".filter-checkbox").each(function(index){ //each is basically for loop, which iterates thru all inputs with class filter-checkbox
            let filter_value = $(this).val() // value of checkbox input
            let filter_key = $(this).data("filter") // data-filter in checkbox input
            console.log(filter_value, filter_key);
            filter_object[filter_key] =
            Array.from(document.querySelectorAll('input[data-filter='+filter_key+']:checked')).map(function // this checks k jehra checkbox checked hai, usko map kia hai fn se,
            (element){
            return element.value // this fn will return value of input field
            })
        })

        $.ajax({
            url: '/filter-products', // here this url will be send to browser url
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                $(".loader").show()
            },
            success: function(res){
                console.log(res);
                $(".loader").show();
                $("#filtered-products").html(res.data);
                $(".numberOfProductsWhileFilter").html(res.totalProductsAfterFilter);
            }
        })
    })
    $(".subscribeBtn").on("click", function(e){
        e.preventDefault();
        document.querySelector('.subscribeBtn').innerText = 'Subscribed';
    })
    //Make Default Address
    $(".make-default-address").on("click", function(e){
        var id=$(this).attr('data-address-id');
        var this_val=$(this);
        // Ajax
        $.ajax({
            url:'/make-default-address', //this send get request
            data:{
                'id':id,
            },
            dataType:'json',
            success:function(response){
                if(response.boolean==true){
                    $(".check").hide();
                    $(".ht_btn").show();
                    $(".check"+id).show();
                    $(".btn"+id).hide();
                }
            }
        });
    })

})

//Add to cart functionality
$(document).on("click", ".add-to-cart-btn", function(){ // if u want to pick id here, that must be unique on one page, otherwise use class
    let cookie = document.cookie
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    console.log("ggn 96")
    let this_val = $(this)
    let index_val = this_val.attr("data-index") //data-index is written by us, u can fetch any attr of html tag in this way
    let dataSource = this_val.attr("data-source") //data-index is written by us, u can fetch any attr of html tag in this way

    let quantity = $(".product-quantity-" + index_val).val() //val() give value of input tag
    let product_title = $(".product-title-" + index_val).val()
    let product_id = index_val
    let product_price = $(".current-product-price-" + index_val).text()
    let product_image = $(".product-image-" + index_val).val()
    data1= {
            'pid': product_id,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
            'image': product_image
        }
    console.log("ggn 104", data1)
    //sending request to server
    $.ajax({
        url: '/add-to-cart/',
        data: {
            'pid': product_id,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
            'image': product_image
        },
        method: 'POST',
        dataType: 'json',
        headers: {
           'X-CSRFToken': csrfToken
         },
        beforeSend: function(){
            console.log("Adding Product to cart..")
        },
        success: function(response){ // if above url te jo code hai , vo shi execute hoga then success chlega
            this_val.html("✔")
            console.log("Added Product to cart !", response.data)
            $(".cart-items-count").text(response.totalCartItems)
            if(typeof dataSource !== 'undefined' && dataSource=="wishlist"){
                let cookie = document.cookie
                let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
                $.ajax({
                    url: "/remove-from-wishlist/",
                    data: {
                        "wishlist_id": product_id
                    },
                    method: 'DELETE',
                    dataType: "json",
                    headers: {
                       'X-CSRFToken': csrfToken
                     },
                    beforeSend: function(){
                        console.log("Deleting...");
                    },
                    success: function(res){
                        $("#wishlist-list").html(res.data)
                        $(".wishlist-main-count").text(res.wishlist_count)
                        console.log("Deleting...", res.wishlist_count);
                    }
                })
            }
        }
    })
})

$(document).on("click", ".delete-product", function(){
    console.log("ggn 128")
    let product_id = $(this).attr("data-product")
    let this_val = $(this)
    console.log("ggn 130", product_id)
    $.ajax({
        url: '/delete-from-cart/',
        data: {    //we send data to above url with this key 'data'
            'id': product_id
        },
        method: 'DELETE',
        dataType: "json",
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalCartItems) //cart icon de uppr jo no circle ch aonda, usnu update
            $('#cart-list').html(response.data)
        }
    })
})

$(document).on("click", ".update-product", function(){
    let product_id = $(this).attr("data-product")
    let product_qty = $(".product-qty-" + product_id).val()
    let this_val = $(this)
    console.log("ggn 153", product_id, product_qty)
    $.ajax({
        url: '/update-cart/',
        data: {    //we send data to above url with this key 'data'
            'id': product_id,
            'product_qty': product_qty
        },
        method: 'PUT',
        dataType: "json",
        beforeSend: function(){
//            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalCartItems) //cart icon de uppr jo no circle ch aonda, usnu update
            $('#cart-list').html(response.data)
        }
    })
})

$(document).on("click", ".add-to-wishlist", function(){
    var product_id = $(this).attr('data-product-item');
    var label = $(this).attr("aria-label")
    var this_val = $(this);
    let cookie = document.cookie
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    console.log(label)
    $.ajax({
        url:"/add-to-wishlist/",
        data:{
        'product_id' : product_id
        },
        method: 'POST',
        dataType:'json',
        headers: {
           'X-CSRFToken': csrfToken
         },
        beforeSend: function(){
            console.log("Adding to wishlist...");
        },
        success:function(response){
            this_val.html("✓")
            if(response.bool == true){
                console.log("Added...");
                $(".wishlist-main-count").text(response.wishlist_count)
            }
        }
    });
})

//remove from wishlist
$(document).on("click", ".delete-wishlist-product", function(){
    let this_val = $(this)
    let wishlist_id = $(this).attr("data-wishlist-product")
    console.log(this_val);
    console.log(wishlist_id);
    $.ajax({
        url: "/remove-from-wishlist/",
        data: {
            "wishlist_id": wishlist_id
        },
        method: 'DELETE',
        dataType: "json",
        beforeSend: function(){
            console.log("Deleting...");
        },
        success: function(res){
            $("#wishlist-list").html(res.data)
            $(".wishlist-main-count").text(res.wishlist_count)
            console.log("Deleting...", res.wishlist_count);
        }
    })
})


