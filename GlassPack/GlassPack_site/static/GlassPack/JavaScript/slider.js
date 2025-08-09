let sliderOne = document.getElementById("slider-1");
let sliderTwo = document.getElementById("slider-2");
let tooltipOne = document.getElementById("tooltip-1");
let tooltipTwo = document.getElementById("tooltip-2");
let minGap = 50; // минимальное расстояние между ползунками

function slideOne() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    tooltipOne.textContent = sliderOne.value;
    moveTooltip(sliderOne, tooltipOne);
    updateTrackColor();
}

function slideTwo() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }
    tooltipTwo.textContent = sliderTwo.value;
    moveTooltip(sliderTwo, tooltipTwo);
    updateTrackColor();
}

function moveTooltip(slider, tooltip) {
    const wrapper = slider.parentElement;
    const sliderWidth = wrapper.offsetWidth;
    const min = parseInt(slider.min);
    const max = parseInt(slider.max);
    const val = parseInt(slider.value);

    const percent = (val - min) / (max - min);
    const position = percent * sliderWidth;

    const tooltipWidth = tooltip.offsetWidth;
    let left = position - tooltipWidth / 2;

    if (left < 0) left = 0;
    if (left + tooltipWidth > sliderWidth) left = sliderWidth - tooltipWidth;

    tooltip.style.left = `${left}px`;
}

function updateTrackColor() {
    const track = document.querySelector(".slider-track");
    if (!track) return;

    const percent1 = (sliderOne.value - sliderOne.min) / (sliderOne.max - sliderOne.min) * 100;
    const percent2 = (sliderTwo.value - sliderTwo.min) / (sliderTwo.max - sliderTwo.min) * 100;
    track.style.background = `linear-gradient(to right, #dadae5 ${percent1}%, #243e7f ${percent1}%, #243e7f ${percent2}%, #dadae5 ${percent2}%)`;
}


document.addEventListener("DOMContentLoaded", function() {
    const checkboxes = document.querySelectorAll('input[name="finish_types"]');
    const form = checkboxes.length > 0 ? checkboxes[0].closest("form") : null;

    if (form) {
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener("change", () => {
                form.submit();
            });
        });
    }
})

function submitForm() {
    document.getElementById("filter-form").submit();
}

window.onload = function () {
    slideOne();
    slideTwo();
};

