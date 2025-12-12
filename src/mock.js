export default async function mockReply(input) {
  // simulate small latency
  await new Promise((r) => setTimeout(r, 600));

  // very simple intent-like greeting detection
  const msg = (input || "").toLowerCase();
  if (/\bhello\b|\bhi\b|\bhey\b/.test(msg)) {
    return {
      reply: "Hello — welcome! How can I help you style an outfit today?",
      recommendations: [],
      images: [],
    };
  }

  if (/\bjeans\b|\bkurta\b|\bdress\b|\btee\b|\bshirt\b|\bkurti\b/.test(msg)) {
    return {
      reply: `Got it — here are a few curated items matching "${input}".`,
      recommendations: [
        {
          sku: "JEANS_001",
          name: "Minimalist Black Jeans",
          brand: "Studio",
          price: 2990,
          image: "https://via.placeholder.com/300x400?text=Black+Jeans",
        },
        {
          sku: "TEE_001",
          name: "White Oversized Tee",
          brand: "Maison",
          price: 1490,
          image: "https://via.placeholder.com/300x400?text=White+Tee",
        },
      ],
      images: ["https://via.placeholder.com/350x500?text=Outfit+1"],
    };
  }

  // fallback
  return {
    reply: "I can help with outfits — tell me what occasion, color or budget you prefer.",
    recommendations: [],
    images: [],
  };
}
