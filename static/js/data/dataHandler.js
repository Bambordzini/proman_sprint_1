export let dataHandler = {
    getBoards: async function () {
        return await apiGet("/api/boards");
    },
    getBoard: async function (boardId) {
        return await apiGet(`/api/boards/${boardId}`);
    },
    getStatuses: async function () {
        return await apiGet('/api/statuses');
    },
    getStatus: async function (statusId) {
        return await apiGet(`/api/statuses/${statusId}`);
    },
    getCardsByBoardId: async function (boardId) {
        return await apiGet(`/api/boards/${boardId}/cards/`);
    },
    getCard: async function (cardId) {
        return await apiGet(`/api/cards/${cardId}`);
    },
    createNewBoard: async function (boardTitle) {
        return await apiPost('/api/boards', { title: boardTitle });
    },
    createNewCard: async function (cardTitle, boardId, statusId) {
        return await apiPost(`/api/boards/${boardId}/cards`, {
            title: cardTitle,
            status_id: statusId
        });
    },
    deleteCard: async function (cardId) {
        return await apiDelete(`/api/cards/${cardId}`);
    },
    updateCard: async function (cardId, newTitle) {
        return await apiPut(`/api/cards/${cardId}`, { title: newTitle });
    },
};

async function apiGet(url) {
    let response = await fetch(url, {
        method: "GET",
    });
    if (response.ok) {
        return await response.json();
    }
}

async function apiPost(url, payload) {
    let response = await fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    if (response.ok) {
        return await response.json();
    }
}

async function apiDelete(url) {
    let response = await fetch(url, {
        method: "DELETE",
    });
    if (response.ok) {
        return response;
    }
}

async function apiPut(url, payload) {
    let response = await fetch(url, {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    if (response.ok) {
        return await response.json();
    }
}
