"""Generated TypedDict models from OpenAPI schemas."""

from __future__ import annotations

from typing import Any, TypedDict

class AICustomerUsage(TypedDict, total=False):
    timestamp: int
    api_version: str
    api_minor_version: str
    status: str
    bsai: BSAI
    user_limits: UserLimits
    usage: Usage

class AIModel(TypedDict, total=False):
    model_id: str
    model_source: str
    display: str

class AIQueryRequest(TypedDict, total=False):
    query: str
    filters: dict[str, Any]

class AIQueryResponse(TypedDict, total=False):
    query: str
    results: QueryResults
    metadata: Metadata

class AISetUsageRequest(TypedDict, total=False):
    input_tokens: int
    output_tokens: int
    requests: int

class AITokensUsage(TypedDict, total=False):
    input_tokens: int
    output_tokens: int
    requests: int

class AccountAuthResponse(TypedDict, total=False):
    authenticated: bool
    authentication_token: str
    refresh_token: str
    refresh_token_invalid: bool
    user_id: int

class AccountDetailsLocation(TypedDict, total=False):
    id: int
    flavor: str
    header: str
    subtext: str
    action_text: str
    subscription_set: int

class AccountSignupRequest(TypedDict, total=False):
    user: str
    password: str
    install_id: str
    supportsAccessToken: int
    subscribe_to_newsletter: str
    implicit_newsletter_consent: str
    first_name: str

class AiInfo(TypedDict, total=False):
    latency_ms: int
    modelInfo: ModelInfo
    usage: AITokensUsage

class AllowSubscriptionPurchase(TypedDict, total=False):
    allow_subscription: bool

class AnalyticsEventsBatch(TypedDict, total=False):
    pass

class AppiraterConfig(TypedDict, total=False):
    pass

class AuthorOrNarrator(TypedDict, total=False):
    name: str
    url: str

class BSAI(TypedDict, total=False):
    enabled: bool

class BookSetVolume(TypedDict, total=False):
    productId: int
    title: str
    volumeNumber: int

class Carousel(TypedDict, total=False):
    title: str
    items: list[CarouselItem]

class CarouselItem(TypedDict, total=False):
    productId: int
    title: str
    image_url: str
    target: str

class CategoriesResponse(TypedDict, total=False):
    categories: list[StoreCategory]

class CategoryResult(TypedDict, total=False):
    categories: list[StoreCategory]
    title: str

class CtaDetail(TypedDict, total=False):
    action: str
    border: str
    button_text: str
    subtitle: str
    title: str
    layout: str
    show_logo: bool

class DailyReadingTemplateVersionsResponse(TypedDict, total=False):
    pass

class DeviceRegistrationRequest(TypedDict, total=False):
    pass

class EmailSignupRequest(TypedDict, total=False):
    email: str
    token: str
    bibles: str

class Feature(TypedDict, total=False):
    feature_name: str
    feature_descr: str
    feature_icon_url: str

class FeatureOfProduct(TypedDict, total=False):
    feature_name: str
    feature_descr: str
    feature_icon_url: str
    feature_icon_dark_url: str

class FirstRunLocation(TypedDict, total=False):
    flavor: str
    subscription_set: int

class ForgotPasswordRequest(TypedDict, total=False):
    email: str

class GatherInterestResponse(TypedDict, total=False):
    need_interests: bool

class HandoffToken(TypedDict, total=False):
    token: str
    error: str

class HeaderSection(TypedDict, total=False):
    type: str
    heading: str
    body: str
    backgroundColor: str
    backgroundDarkColor: str
    trial_visibility: str

class LibraryBarLocation(TypedDict, total=False):
    id: int
    flavor: str
    subscription_set: int

class MainMenuLocation(TypedDict, total=False):
    flavor: str
    layout: str
    title: str
    body: str
    subscription_set: int

class MediumAds(TypedDict, total=False):
    title: str
    target: str
    image_url: str

class Message(TypedDict, total=False):
    id: int
    read: bool
    title: str
    body: str

class MessageMetricsRequest(TypedDict, total=False):
    install_id: str
    message_id: int
    metrics: dict[str, Any]

class MessagesRequest(TypedDict, total=False):
    install_id: str

class MessagesResponse(TypedDict, total=False):
    messages: list[Message]

class Metadata(TypedDict, total=False):
    ai_info: AiInfo
    api_version: str
    app: str
    cache_hit: bool
    current_day_idx: int
    daily_requests_used: int
    host: str
    query_hash: str
    rolling_tokens_used: int
    timestamp: int

class ModelInfo(TypedDict, total=False):
    model_id: str
    model_source: str

class NeedInterestsResponse(TypedDict, total=False):
    need_interests: bool

class PrivacySessionStart(TypedDict, total=False):
    pass

class Product(TypedDict, total=False):
    productId: int
    title: str
    subtitle: str
    publisher: str
    productForm: ProductFormEnum
    list_price: str
    our_price: str
    is_available: bool
    isFree: bool
    owns_product: bool
    coverImageUrl: str
    authors: list[str]
    bundledIds: list[int]
    textProductIds: list[int]

class ProductDetail2(TypedDict, total=False):
    productId: int
    title: str
    publisher: str
    list_price: str
    our_price: str
    is_available: bool
    isFree: bool
    owns_product: bool
    productForm: ProductFormEnum
    authors: list[AuthorOrNarrator]
    narrators: list[AuthorOrNarrator]
    audioProductIds: list[int]
    textProductIds: list[int]
    audioDuration: int
    bookSetId: int
    features: list[FeatureOfProduct]
    related: list[RelatedProduct]
    coverImageUrl: str
    description: str
    sampleUrl: str

class ProductFormEnum(TypedDict, total=False):
    pass

class ProductListItem(TypedDict, total=False):
    dollar_type: str
    type: str
    productId: int
    title: str
    publisher: str
    list_price: str
    our_price: str
    is_available: bool
    isFree: bool
    owns_product: bool
    productForm: ProductFormEnum
    authors: list[AuthorOrNarrator]
    narrators: list[AuthorOrNarrator]
    audioProductIds: list[int]
    textProductIds: list[int]
    bundledIds: list[int]
    inSubscriptionIds: list[int]
    bookSetId: str
    newVersionProductId: str
    preferredAudioRelation: str
    webstoreCTAAvailable: bool
    bookSetUpgradesAvailable: list[int]
    priceTierId: str
    image_url: str

class ProductSet(TypedDict, total=False):
    dollar_type: str
    title: str
    page_index: int
    pages: int
    total_count: int
    product_results: list[ProductListItem]
    filters: list[SVFilter]
    sort_options: list[SVSortItem]
    paid: bool
    more_paid: bool

class ProductSetArray(TypedDict, total=False):
    dollar_type: str
    sections: list[ProductSet]

class ProductSliderSection(TypedDict, total=False):
    type: str
    products: list[ProductListItem]
    brandLogoURL: str
    backgroundColor: str
    textColor: str

class PromoColors(TypedDict, total=False):
    lowerPaint: str
    midPaint: str
    upperPaint: str
    overPaintText: str
    textOverWhite: str

class PurchaseDetails(TypedDict, total=False):
    backgroundColor: str
    backgroundDarkColor: str
    buttonColor: str
    buttonTextColor: str
    textColor: str
    annualUnderButtonText: str

class QueryResults(TypedDict, total=False):
    verse_references: list[str]
    actual_search: str
    suggested: list[str]
    message: str

class RecommendedProduct(TypedDict, total=False):
    productId: int
    title: str
    list_price: str
    our_price: str
    owns_product: bool
    isFree: bool
    productForm: ProductFormEnum
    bundledIds: list[int]

class RegisterProductsRequest(TypedDict, total=False):
    pass

class RegisterSubscriptionRequest(TypedDict, total=False):
    signupSource: str
    receiptData: str
    subscriptionProductId: str
    platformToken: str
    packageName: str

class RelatedProduct(TypedDict, total=False):
    productId: int
    title: str
    productForm: ProductFormEnum
    list_price: str
    our_price: str

class RelatedSet(TypedDict, total=False):
    title: str
    products: list[RelatedProduct]

class ResourceGuideLocation(TypedDict, total=False):
    id: int
    flavor: str
    header: str
    subtext: str
    action_text: str
    subscription_set: int

class SVFilter(TypedDict, total=False):
    title: str
    description: str
    items: list[SVFilterItem]

class SVFilterItem(TypedDict, total=False):
    id: int
    label: str
    description: str
    match_count: int
    set_id: int

class SVSortItem(TypedDict, total=False):
    id: str
    display: str
    current: bool

class SaleBanner(TypedDict, total=False):
    title: str
    url: str
    style: str

class SmartSearchError(TypedDict, total=False):
    error: str
    errorCode: str
    usage_resets: str

class StoreBookSetVolume(TypedDict, total=False):
    productId: int
    title: str
    owns_product: bool

class StoreCategory(TypedDict, total=False):
    id: int
    title: str
    target: str
    image_url: str

class StoreHomeFeed(TypedDict, total=False):
    rows: list[StoreRow]

class StoreHomeLocation(TypedDict, total=False):
    flavor: str
    layout: str
    title: str
    subtitle: str
    subscription_set: int

class StoreItem(TypedDict, total=False):
    dollar_type: str
    id: int
    productId: int
    title: str
    target: str
    image_url: str
    list_price: str
    our_price: str
    is_available: bool
    isFree: bool
    owns_product: bool
    productForm: ProductFormEnum
    authors: list[AuthorOrNarrator]
    narrators: list[AuthorOrNarrator]
    publisher: str
    bundledIds: list[int]
    audioProductIds: list[int]
    textProductIds: list[int]
    inSubscriptionIds: list[int]
    forceBrowser: bool
    webstoreCTAAvailable: bool

class StoreRow(TypedDict, total=False):
    type: str
    title: str
    display: str
    see_all_target: str
    items: list[StoreItem]

class Subscription(TypedDict, total=False):
    subscriptionProductId: int
    title: str
    abbrTitle: str
    flavor: str
    defaultBillingId: int
    trialEligible: bool
    sections: list[dict[str, Any]]
    purchaseDetails: dict[str, Any]
    promoColors: dict[str, Any]

class SubscriptionLocations(TypedDict, total=False):
    store_home: StoreHomeLocation
    main_menu: MainMenuLocation
    library_bar: LibraryBarLocation
    first_run: FirstRunLocation
    resource_guide: ResourceGuideLocation
    account_details: AccountDetailsLocation

class SubscriptionMarketing(TypedDict, total=False):
    locations: dict[str, Any]

class SyncReleaseLockResponse(TypedDict, total=False):
    success: bool

class SyncStatusResponse(TypedDict, total=False):
    customer: dict[str, Any]
    server: dict[str, Any]

class TextSection(TypedDict, total=False):
    type: str
    body: str
    backgroundColor: str
    backgroundDarkColor: str

class Usage(TypedDict, total=False):
    daily_requests_used: int
    rolling_tokens_used: int

class UserLimits(TypedDict, total=False):
    daily_requests: int
    rolling_tokens: int

class VerseOfTheDayResult(TypedDict, total=False):
    title: str
    text: str
    url: str
    verses: str
    date: str
    productId: int
    timestamp: int
    image_url: str
    translation: str

class VerseReferenceItem(TypedDict, total=False):
    verse: str
    score: str
    verseText: str

class WhatsIncludedProduct(TypedDict, total=False):
    productId: int
    title: str
    productForm: ProductFormEnum

class WishList(TypedDict, total=False):
    id: int
    title: str

class WishListData(TypedDict, total=False):
    wishlists: list[WishList]
