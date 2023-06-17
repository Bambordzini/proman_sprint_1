import {dataHandler} from "../data/dataHandler.js";
import {htmlFactory, htmlTemplates} from "../view/htmlFactory.js";
import {domManager} from "../view/domManager.js";
import Sortable from 'sortablejs';

export let cardsManager = {
    loadCards: async function (boardId) {
        const cards = await dataHandler.getCardsByBoardId(boardId);
        for (let card of cards) {
            const cardBuilder = htmlFactory(htmlTemplates.card);
            const content = cardBuilder(card);
            domManager.addChild(`.board[data-board-id="${boardId}"]`, content);

            // Dodaj obsługę kliknięcia na tytuł karty, aby go edytować
            domManager.addEventListener(
                `.card[data-card-id="${card.id}"] .card-title`,
                "click",
                this.handleCardTitleClick
            );
        }

        // Utwórz nowy Sortable na kolumnach tablicy
        new Sortable(document.querySelector(`.board[data-board-id="${boardId}"] .columns`), {
            group: 'shared', // Dzięki temu karty można przeciągać między kolumnami
            animation: 150,
            onEnd: this.handleCardDrop,
        });
    },

    handleCardTitleClick: async function (event) {
        const cardElement = event.target.closest('.card');
        const cardId = cardElement.dataset.cardId;
        const originalTitle = cardElement.querySelector('.card-title').textContent;

        // Zmień tytuł karty na pole wprowadzania
        const inputElement = document.createElement('input');
        inputElement.type = 'text';
        inputElement.value = originalTitle;
        inputElement.addEventListener('blur', handleCardTitleChange);
        inputElement.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                event.target.blur(); // Wywołuje handleCardTitleChange
            } else if (event.key === 'Escape') {
                event.target.value = originalTitle; // Przywraca oryginalny tytuł
                event.target.blur(); // Wywołuje handleCardTitleChange
            }
        });
        cardElement.replaceChild(inputElement, cardElement.querySelector('.card-title'));

        async function handleCardTitleChange(event) {
            const newTitle = event.target.value;
            const response = await dataHandler.updateCardTitle(cardId, newTitle);
            if (response.ok) {
                // Zmień pole wprowadzania z powrotem na tytuł karty
                const titleElement = document.createElement('div');
                titleElement.classList.add('card-title');
                titleElement.textContent = newTitle;
                titleElement.addEventListener('click', cardsManager.handleCardTitleClick);
                cardElement.replaceChild(titleElement, event.target);
            } else {
                console.error(`Failed to update title of card with id ${cardId}`);
            }
        }
    },

    handleCardDrop: async function (event) {
        const cardId = event.item.dataset.cardId;
        const newColumnId = event.to.dataset.columnId;
        const newIndex = [...event.to.children].indexOf(event.item);
        const response = await dataHandler.updateCardStatusAndOrder(cardId, newColumnId, newIndex);
        if (!response.ok) {
            console.error(`Failed to update status and order of card with id ${cardId}`);
        }
    },
};
