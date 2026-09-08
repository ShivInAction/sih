"""UI rendering and interaction package."""
from src.ui.audio import inject_mic_component
from src.ui.cards import (
    format_disease_card_html,
    format_seasonal_prevention_card,
    care_pathway_html,
    emergency_banner_html,
    caution_banner_html,
    generate_telemedicine_guide,
    generate_maternal_child_module,
    generate_jan_aushadhi_guide,
    generate_asha_anm_guide,
    generate_district_locator_results,
    generate_ranked_facility_results,
    generate_schemes_guide,
    render_abha_html,
    render_health_camps_html,
    render_helpline_guide,
    format_trauma_emergency_card,
    format_general_clinical_triage_card,
    render_debug_panel,
    render_medicine_showcase_grid,
)
from src.ui.pipeline import generate_response
from src.ui.views import (
    _ui,
    render_navbar,
    render_sidebar,
    render_hero,
    render_feature_highlights,
    render_statistics_ribbon,
    render_why_choose_us,
    render_testimonial_section,
    render_tabs,
    render_visibility_fix,
    render_footer,
)
