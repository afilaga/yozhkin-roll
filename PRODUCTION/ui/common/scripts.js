/* === EZHKIN COMMON SCRIPTS === */
/* Contains: Cart Opening Logic, Interactions */

// === PLAN B: ROBUST CART OPENER ===
function novaOpenCart(btn) {
    // 1. Попытка нажать на родную иконку Тильды (самый надежный способ)
    const tildaWidget = document.querySelector('.t706__carticon');
    if (tildaWidget) {
        console.log('Nova: Clicking native Tilda widget...');
        tildaWidget.click();

        // Маленький хак: если Тильда виджет скрыт, клик может не пройти
        // В таком случае пробуем метод 2
        setTimeout(() => {
            const cartWindow = document.querySelector('.t706__cartwin');
            if (!cartWindow || getComputedStyle(cartWindow).opacity === '0') {
                tryOpenDirectly();
            }
        }, 100);
        return;
    }

    tryOpenDirectly();
}

function tryOpenDirectly() {
    console.log('Nova: Trying direct open...');
    // 2. Прямой вызов функции
    if (typeof t706_showPopup === 'function') {
        t706_showPopup();
        return;
    }

    // 3. Переход по хэшу (иногда Тильда слушает это)
    window.location.href = '#order';

    // 4. Если совсем ничего не помогло - ищем ссылки
    const orderLinks = document.querySelectorAll('a[href="#order"]');
    for (let link of orderLinks) {
        // Не нажимаем на саму себя
        if (link.className.includes('nova-icon-btn')) continue;
        link.click();
        return;
    }
}
