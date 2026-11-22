// Edit the numbered gifts here. The temple and simple list both use this catalog.
const giftBoxCount = 100;
const numberedGiftNodes = {
  why:{number: 1, title: 'The Gift of Understanding Why Jesus Gives the Gifts of God',description:'Jesus gives the gifts of God to woo us into loving Him more: the First Great Commandment made personal.',children:['marvel'],url:'gift-1-why-jesus-gives-the-gifts-of-god.html'},
  restaurant:{number: 2, title: 'Jesus Mountain Restaurant',description:'A restaurant within the temple, containing practical and spiritual gifts for family life.',children:['meals','food','patio'],url:'inheritance-map.html'},
  tv:{number: 3, title: 'Jesus TV — The Living Station',description:'Greg as receiver and broadcaster; Greg and Jesus watch life together. A growing treasury of redeemed songs and performance scenes.',children:['songs','broadcast','scenes'],url:'../jesus-tv/'},
  telepathy:{number: 4, title: 'Jesus Telepathy',description:'Jesus and I can communicate without opening our mouths.',children:['marvel']},
  marvel:{number: 5, title: 'Marveling at the Gifts of God',description:'Jesus gives me the gift of marveling at what He gives me.',children:['telepathy','songs']}
};
const numberedGifts = Object.entries(numberedGiftNodes)
  .sort(([, first], [, second]) => first.number - second.number);
