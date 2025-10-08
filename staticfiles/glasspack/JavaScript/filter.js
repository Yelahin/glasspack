document.addEventListener("DOMContentLoaded", function() {
    const checkboxes = document.querySelectorAll('input[name="finish_types"], input[name="colors"]');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            const urlParams = new URLSearchParams(window.location.search);

            urlParams.delete('finish_types');
            urlParams.delete('colors');

            checkboxes.forEach(cb => {
                if (cb.checked) {
                    urlParams.append(cb.name, cb.value);
                }
            });

            urlParams.set("page", 1);

            window.location.search = urlParams.toString();
        });
    });
});