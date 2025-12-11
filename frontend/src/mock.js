export default async function mockReply(input) {
  return {
    reply: "Here are some luxury recommendations.",
    recommendations: [
      {
        name: "Minimalist Black Jeans",
        brand: "ZARA",
        price: 2990,
        image: "https://via.placeholder.com/300x400"
      },
      {
        name: "White Oversized Tee",
        brand: "H&M",
        price: 1490,
        image: "https://via.placeholder.com/300x400"
      }
    ],
    images: [
      "https://via.placeholder.com/350x500"
    ]
  };
}
