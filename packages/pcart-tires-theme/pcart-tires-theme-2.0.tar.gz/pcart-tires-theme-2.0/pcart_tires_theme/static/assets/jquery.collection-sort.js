! function($) {
    function initialize() {
        switch ($.cookie("productsGridList")) {
            case "grid":
                $("#toggle_grid").addClass("active");
                $("#toggle_list").removeClass("active");
                $(".product_listing_main").removeClass("view_list");
                break;
            case "list":
                $("#toggle_grid").removeClass("active");
                $("#toggle_list").addClass("active");
                $(".product_listing_main").addClass("view_list");
                break;
            default:
                $.cookie("productsGridList", "grid", {
                    expires: 365
                });
        }

        $("#toggle_grid").on("click", function() {
            $.cookie("productsGridList", "grid", {
                expires: 365
            });
            if(!$(this).hasClass("active")) {
                $("#toggle_list").removeClass("active");
                $(this).addClass("active");
                $(".product_listing_main").removeClass("view_list");
            }
        });
        $("#toggle_list").on("click", function() {
            $.cookie("productsGridList", "list", {
                expires: 365
            });
            if(!$(this).hasClass("active")) {
                $("#toggle_grid").removeClass("active");
                $(this).addClass("active");
                $(".product_listing_main").addClass("view_list");
            }
        });
    }

    initialize();

//    function i(i, o) {
//        function s() {
//            e("#pagination a").each(function() {
//                var c = e(this).attr("href").replace(/.*page=/, "").replace(/\&.*/, "");
//                e(this).attr("href", a + "&page=" + c), e(this).click(function() {
//                    return e("#collection_sorted").load(e(this).attr("href") + " #collection_sorted > *", function() {
//                        e.cookie("productsQuantity", i), e.cookie("productsSort", o), t(), s(), e("#product_listing_preloader").fadeOut(300), e("#collection_sorted").animate({
//                            opacity: 1
//                        }, 500)
//                    }), !1
//                })
//            })
//        }
//        var a = window.location.toString();
//        a = a.indexOf("view") > -1 ? a.replace(/.*view/, "").indexOf("&") > -1 ? a.replace(/view=.*?&/, "view=" + i + "&") : a.replace(/view=.*/, "view=" + i) : a.indexOf("?") > -1 ? a + "&view=" + i : a + "?view=" + i, a = a.indexOf("sort_by") > -1 ? a.replace(/.*sort_by/, "").indexOf("&") > -1 ? a.replace(/sort_by=.*?&/, "sort_by=" + o + "&") : a.replace(/sort_by=.*/, "sort_by=" + o) : a.indexOf("?") > -1 ? a + "&sort_by=" + o : a + "?sort_by=" + o, a.indexOf("page") > -1 ? a = a.replace(/.*page/, "").indexOf("&") > -1 ? a.replace(/page=.*?&/, "page=1&") : a.replace(/page=.*/, "page=1") : a += a.indexOf("?") > -1 ? "&page=1" : "?page=1", e("#product_listing_preloader").fadeIn(600), e("#collection_sorted").animate({
//            opacity: 0
//        }, 400), e("#collection_sorted").load(a + " #collection_sorted > *", function() {
//            e.cookie("productsQuantity", i), e.cookie("productsSort", o), t(), s(), e("#product_listing_preloader").fadeOut(300), e("#collection_sorted").animate({
//                opacity: 1
//            }, 500)
//        })
//    }

//    function o(t) {
//        e("#show_products_select option").each(function() {
//            e(this).val() == t && e(this).attr("selected", "selected")
//        })
//    }

//    function s(t) {
//        e("#sort_by_select option").each(function() {
//            e(this).val() == t && e(this).attr("selected", "selected")
//        })
//    }
//    e("#product_listing_preloader").hide(), e(document).ready(function() {
//        var a = e.cookie("productsQuantity"),
//            c = e.cookie("productsSort");
//        t(), a && c ? (i(a, c), o(a), s(c)) : a && !c ? (i(a, "manual"), o(a), s("manual")) : !a && c ? (i(6, c), o(6), s(c)) : (i(6, "manual"), o(6), s("manual")), e("#show_products_select").on("change", function() {
//            i(e(this).val(), e("#sort_by_select").val())
//        }), e("#sort_by_select").on("change", function() {
//            i(e("#show_products_select").val(), e(this).val())
//        })
//    })
    $("#sort_by_select").change(function() {
        // Add hidden input because disabled select box is not submitting
        $(this).parent().append('<input type="hidden" name="sort" value="'+$(this).val()+'">');
        $(this).prop("disabled", true);
        $(this).parent().submit();
    });

}(jQuery);