// File: frontend/src/locales/messages.js

export const messages = {
  vi_VN: {
    // Header & Global
    brandName: 'Bộ Tính CDR LMHT',
    brandSubtitle: 'Hệ Thống Tính Toán Thời Gian Hồi Chiêu',
    patch: 'Phiên bản',
    syncCdn: 'Đồng bộ CDN',
    syncing: 'Đang đồng bộ...',
    syncFailed: 'Đồng bộ thất bại',
    syncedPatch: 'Đã đồng bộ phiên bản',
    resetBuild: 'Đặt lại Build',
    loadingData: 'Đang tải dữ liệu chiến thuật...',
    footerText: 'League of Legends CDR Engine • Tính toán chuẩn xác dưới 50ms • Clean Architecture & DDD',

    // Champion Selector
    championTitle: 'Tướng',
    championSearchPlaceholder: 'Tìm kiếm tướng...',
    selectChampionPrompt: 'Chọn một vị tướng để bắt đầu',
    noChampionsFound: 'Không tìm thấy tướng phù hợp',

    // Ability Panel
    abilityTitle: 'Kỹ Năng & Cấp Độ',
    qwerStepper: 'Tăng cấp Q / W / E / R',
    baseCooldown: 'Hồi chiêu gốc',
    finalCooldown: 'Hồi chiêu thực',
    rank: 'Cấp',
    base: 'Gốc',
    selectChampionAbilities: 'Chọn một vị tướng để cấu hình cấp độ kỹ năng',
    cooldownSec: 'giây',

    // Item Inventory
    itemTitle: 'Trang Bị',
    itemSearchPlaceholder: 'Tìm trang bị theo tên...',
    emptySlot: 'Ô trống',
    totalItemHaste: 'Tổng Haste Trang Bị',
    goldCost: 'Vàng',
    remove: 'Gỡ bỏ',
    allItems: 'Tất cả trang bị',
    noItemsFound: 'Không tìm thấy trang bị',

    // Runes
    runeTitle: 'Ngọc Bổ Trợ & Mảnh',
    runeStacks: 'Cộng dồn',
    activeRunes: 'Đã chọn',
    selectedRunesCount: 'đã chọn',
    maxStacks: 'Tối đa',
    perStack: 'mỗi dồn',

    // Summoner Spells
    spellTitle: 'Phép Bổ Trợ',
    spellSlot1: 'Phép 1',
    spellSlot2: 'Phép 2',
    selectSpell: 'Chọn phép',
    twoSlots: '2 Ô phép',
    selectSummonerSpell: 'Chọn Phép Bổ Trợ',

    // Cooldown Summary / Telemetry
    summaryTitle: 'Tổng Kết Hồi Chiêu',
    telemetryTitle: 'Báo Cáo Telemetry',
    originalCd: 'Ban đầu',
    reducedCd: 'Sau giảm',
    cdrPercentage: 'Giảm',
    hasteBreakdown: 'Phân Tích Chỉ Số Haste',
    generalHaste: 'Hồi Kỹ Năng',
    ultHaste: 'Hồi Chiêu Cuối',
    basicHaste: 'Hồi Kỹ Năng Cơ Bản',
    summHaste: 'Hồi Phép Bổ Trợ',
    calculating: 'Đang tính toán...',
    liveAuthoritative: 'Tính toán trực tiếp',
    noActiveTelemetry: 'Chưa có dữ liệu tính toán của tướng',
    summonerSpellsTelemetry: 'Báo Cáo Phép Bổ Trợ',
  },

  en_US: {
    // Header & Global
    brandName: 'LoL CDR Engine',
    brandSubtitle: 'Tactical Cooldown Calculator Core',
    patch: 'Patch',
    syncCdn: 'Sync CDN',
    syncing: 'Syncing...',
    syncFailed: 'Sync failed',
    syncedPatch: 'Synced patch',
    resetBuild: 'Reset Build',
    loadingData: 'Loading Tactical Data...',
    footerText: 'League of Legends CDR Engine • Authoritative Sub-50ms Calculation • DDD & Clean Architecture',

    // Champion Selector
    championTitle: 'Champion',
    championSearchPlaceholder: 'Search champions...',
    selectChampionPrompt: 'Select a champion to begin',
    noChampionsFound: 'No champions found',

    // Ability Panel
    abilityTitle: 'Abilities & Skill Ranks',
    qwerStepper: 'Q / W / E / R Stepper',
    baseCooldown: 'Base CD',
    finalCooldown: 'Final CD',
    rank: 'Rank',
    base: 'Base',
    selectChampionAbilities: 'Select a champion to configure skill ranks',
    cooldownSec: 's',

    // Item Inventory
    itemTitle: 'Item Loadout',
    itemSearchPlaceholder: 'Search items by name...',
    emptySlot: 'Empty Slot',
    totalItemHaste: 'Total Item Haste',
    goldCost: 'Gold',
    remove: 'Remove',
    allItems: 'Available Items',
    noItemsFound: 'No items found',

    // Runes
    runeTitle: 'Haste Runes & Shards',
    runeStacks: 'Stacks',
    activeRunes: 'Active Runes',
    selectedRunesCount: 'Selected',
    maxStacks: 'Max',
    perStack: 'stack',

    // Summoner Spells
    spellTitle: 'Summoner Spells',
    spellSlot1: 'Spell 1',
    spellSlot2: 'Spell 2',
    selectSpell: 'Select spell',
    twoSlots: '2 Slots',
    selectSummonerSpell: 'Select Summoner Spell',

    // Cooldown Summary / Telemetry
    summaryTitle: 'Cooldown Summary',
    telemetryTitle: 'Cooldown Telemetry',
    originalCd: 'Original',
    reducedCd: 'Reduced',
    cdrPercentage: 'CDR',
    hasteBreakdown: 'Haste Breakdown',
    generalHaste: 'Ability Haste',
    ultHaste: 'Ult Haste',
    basicHaste: 'Basic Haste',
    summHaste: 'Summ. Haste',
    calculating: 'Calculating...',
    liveAuthoritative: 'Live Authoritative',
    noActiveTelemetry: 'No active champion telemetry',
    summonerSpellsTelemetry: 'Summoner Spells Telemetry',
  },
}
