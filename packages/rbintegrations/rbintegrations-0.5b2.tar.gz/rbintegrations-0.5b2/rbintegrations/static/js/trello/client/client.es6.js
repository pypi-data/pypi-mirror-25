const WHITE_ICON = 'https://cdn.hyperdev.com/us-east-1%3A3d31b21c-01a0-4da2-8827-4bc6e88b7618%2Ficon-white.svg';

TrelloPowerUp.initialize({
    'board-buttons': (t, options) => {
        return [
            {
                icon: WHITE_ICON,
                text: 'Review Board',
                callback: () => {},
            },
        ];
    },
});
