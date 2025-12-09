from pydantic import BaseModel
from typing import List, Optional, Dict


class Product(BaseModel):
    sku: str
    name: str
    category: str
    sub_category: str
    brand: str
    gender: str
    fit: str
    occasion: List[str]
    style_tags: List[str]
    base_color: str
    sizes: List[str]
    material: str
    season: str
    price: int
    currency: str
    images: List[str]
    tags: List[str]


class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    phone: str
    city: str
    preferred_store_id: str
    loyalty_tier: str
    loyalty_points: int
    device_preferences: List[str]
    primary_style: str
    preferred_occasion_focus: List[str]
    color_preferences: List[str]
    size_profile: Dict[str, str]
    channel_last_seen: str
    last_active_at: str


class InventoryItem(BaseModel):
    sku: str
    store_id: str
    store_name: str
    store_type: str
    quantity_available: int
    last_updated: str


class CartItem(BaseModel):
    sku: str
    quantity: int
    size: Optional[str] = None


class LoyaltyRule(BaseModel):
    tier: str
    points_per_rupee: float
    min_points_to_redeem: int
    max_discount_percent_via_points: float


class Promotion(BaseModel):
    promo_code: str
    description: str
    discount_type: str
    discount_value: float
    applicable_categories: List[str]
    applicable_sub_categories: List[str]
    min_order_value: int
    start_date: str
    end_date: str
    applicable_channels: List[str]
    max_uses_per_customer: int


class LoyaltyQuoteRequest(BaseModel):
    customer_id: str
    items: List[CartItem]
    channel: str
    applied_promo_code: Optional[str] = None
    loyalty_tier: Optional[str] = None
    loyalty_points_available: Optional[int] = None


class LoyaltyQuoteResponse(BaseModel):
    subtotal: float
    promo_code: Optional[str]
    promo_discount: float
    loyalty_points_available: int
    loyalty_points_to_use: int
    loyalty_discount: float
    total_payable: float
    loyalty_points_to_earn: int
    summary_text: str


class Order(BaseModel):
    order_id: str
    customer_id: str
    channel: str
    order_type: str
    store_id: Optional[str]
    order_status: str
    payment_status: str
    payment_method: str
    total_amount: float
    currency: str
    discount_amount: float
    loyalty_points_used: int
    loyalty_points_earned: int
    created_at: str
    updated_at: str


class OrderItem(BaseModel):
    order_item_id: str
    order_id: str
    sku: str
    quantity: int
    unit_price: float
    final_price: float


class Payment(BaseModel):
    payment_id: str
    order_id: str
    customer_id: str
    amount: float
    currency: str
    status: str
    method: str
    gateway_reference: str
    failure_reason: Optional[str]
    created_at: str


class BrowsingEvent(BaseModel):
    event_id: str
    customer_id: str
    channel: str
    event_type: str
    sku: Optional[str]
    search_query: Optional[str]
    timestamp: str
