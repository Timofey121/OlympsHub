$(function () {
    $(".account_cont").click(function () {
        $(".open_menu_arrow_cont").toggleClass("open_menu_arrow_active");
        $(".open_menu_cont").toggleClass("open_menu_cont_active");
    });
});
$(function () {
    $(".icon_menu").click(function () {
        $(".nav").toggleClass("nav_active");
        $(".nav_mobile").toggleClass("nav_mobile_active");
        $(".connect_container").removeClass("connect_container_active");
    });
});
$(function () {
    $(".accout_svg_disactive").click(function () {
        $(".connect_container").toggleClass("connect_container_active");
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelector('.navigation_links'); // Основное меню
    const navLinksMobile = document.querySelector('.navigation_links_mobile'); // Мобильное меню
    const registerButton = document.querySelector('.account_button'); // Кнопка "Регистрация"

    function moveElementsToMobileMenu() {
        if (window.innerWidth < 700) {
            // Перемещаем кнопку "Регистрация" в мобильное меню
            if (registerButton && !navLinksMobile.contains(registerButton)) {
                navLinksMobile.appendChild(registerButton);
                registerButton.classList.add('mobile_register_button'); // Добавляем стиль
            }
        } else {
            // Возвращаем кнопку обратно в основное меню
            if (registerButton && !navLinks.contains(registerButton)) {
                navLinks.appendChild(registerButton);
                registerButton.classList.remove('mobile_register_button'); // Убираем стиль
            }
        }
    }

    // Вызываем при загрузке страницы
    moveElementsToMobileMenu();

    // Отслеживаем изменение размера экрана
    window.addEventListener('resize', moveElementsToMobileMenu);
});

$('body').on('click', '.icon_hide', function () {
    if ($('#password_input').attr('type') == 'password') {
        $(this).addClass('view');
        $('#password_input').attr('type', 'text');
    } else {
        $(this).removeClass('view');
        $('#password_input').attr('type', 'password');
    }
    return false;
});
