# Generated by Django 5.1.4 on 2024-12-27 11:20

from django.db import migrations, models
import datetime

PUBLICATION_DATES = dict(
    [
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-con-konzeption-und-vorgehensweisen",
            datetime.date(2024, 5, 18),
        ),
        (
            "urn:intuitem:risk:library:risk-matrix-5x5-sensitive",
            datetime.date(2024, 5, 4),
        ),
        ("urn:intuitem:risk:library:owasp-top-10-web", datetime.date(2024, 3, 2)),
        ("urn:intuitem:risk:library:owasp-masvs-v2.1.0", datetime.date(2024, 5, 25)),
        (
            "urn:protocolpaladin:risk:library:matrice-des-risques-critiques-3x3",
            datetime.date(2024, 5, 11),
        ),
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-ind-industrielle-it",
            datetime.date(2024, 5, 18),
        ),
        ("urn:intuitem:risk:library:aircyber-v1.5.2", datetime.date(2024, 4, 9)),
        ("urn:intuitem:risk:library:rgs-v2.0", datetime.date(2024, 4, 7)),
        ("urn:intuitem:risk:library:cra-proposal-annexes", datetime.date(2024, 4, 11)),
        ("urn:intuitem:risk:library:iso27001-2022", datetime.date(2024, 3, 2)),
        (
            "urn:intuitem:risk:library:mapping-iso27001-2013-to-iso27001-2022",
            datetime.date(2024, 7, 9),
        ),
        ("urn:intuitem:risk:library:enisa-5g-scm-v1.3", datetime.date(2024, 5, 18)),
        ("urn:intuitem:risk:library:cnil-guide-securite", datetime.date(2024, 12, 14)),
        (
            "urn:protocolpaladin:risk:library:anssi-recommandations-securite-architecture-systeme-journalisation",
            datetime.date(2024, 8, 4),
        ),
        ("urn:intuitem:risk:library:anssi-guide-hygiene", datetime.date(2024, 4, 18)),
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-net-netze-und-kommunikation",
            datetime.date(2024, 5, 18),
        ),
        (
            "urn:intuitem:risk:library:rts-dora-ictservices-supporting",
            datetime.date(2024, 6, 13),
        ),
        (
            "urn:intuitem:risk:library:itar-compliance-program-guidelines",
            datetime.date(2024, 12, 21),
        ),
        ("urn:intuitem:risk:library:FNCS-v2", datetime.date(2024, 11, 9)),
        ("urn:intuitem:risk:library:nis2-directive", datetime.date(2024, 2, 11)),
        ("urn:intuitem:risk:library:sama-csf-1.0", datetime.date(2024, 12, 1)),
        ("urn:intuitem:risk:library:scf-2024-2", datetime.date(2024, 6, 30)),
        (
            "urn:intuitem:risk:library:risk-matrix-5x5-iso27005",
            datetime.date(2024, 7, 22),
        ),
        (
            "urn:intuitem:risk:library:bsi-externer-cloud-dienste",
            datetime.date(2024, 10, 14),
        ),
        ("urn:intuitem:risk:library:nist-ai-rmf-1.0", datetime.date(2024, 3, 23)),
        ("urn:intuitem:risk:library:mitre-attack", datetime.date(2024, 2, 11)),
        ("urn:intuitem:risk:library:tisax-v5.1", datetime.date(2024, 6, 18)),
        ("urn:intuitem:risk:library:bsi-c5-2020", datetime.date(2024, 9, 29)),
        (
            "urn:intuitem:risk:library:anssi-genai-security-recommendations-1.0",
            datetime.date(2024, 5, 1),
        ),
        ("urn:intuitem:risk:library:fadp", datetime.date(2024, 4, 21)),
        (
            "urn:intuitem:risk:library:risk-matrix-4x4-ebios-rm",
            datetime.date(2024, 11, 29),
        ),
        (
            "urn:intuitem:risk:library:rts-dora-incident-reporting",
            datetime.date(2024, 8, 12),
        ),
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-app-anwendungen",
            datetime.date(2024, 5, 18),
        ),
        ("urn:intuitem:risk:library:nist-sp-800-66-rev2", datetime.date(2024, 4, 5)),
        (
            "urn:protocolpaladin:risk:library:mapping-secnumcloud-3.2-to-iso27001-2022",
            datetime.date(2024, 10, 30),
        ),
        (
            "urn:intuitem:risk:library:anssi-maturite-gestion-crise-1.0.2",
            datetime.date(2024, 5, 18),
        ),
        (
            "urn:intuitem:risk:library:secnumcloud-3.2-annexe-2",
            datetime.date(2024, 5, 9),
        ),
        ("urn:intuitem:risk:library:ccb-cff-2023-03-01", datetime.date(2024, 4, 5)),
        (
            "urn:intuitem:risk:library:annex-technical-and-methodological-requirements-nis2",
            datetime.date(2024, 10, 26),
        ),
        ("urn:intuitem:risk:library:ccpa_act", datetime.date(2024, 7, 2)),
        (
            "urn:intuitem:risk:library:rts-dora-threat-led-penetration-tests",
            datetime.date(2024, 8, 12),
        ),
        ("urn:intuitem:risk:library:dnssi-2023-2", datetime.date(2024, 7, 18)),
        (
            "urn:intuitem:risk:library:cyber_essentials_requirements_for_it_infrastructure",
            datetime.date(2024, 7, 9),
        ),
        (
            "urn:intuitem:risk:library:risk-matrix-4x4-with-5-levels",
            datetime.date(2024, 7, 28),
        ),
        (
            "urn:intuitem:risk:library:its-dora-incident-reporting",
            datetime.date(2024, 8, 12),
        ),
        (
            "urn:intuitem:risk:library:formulaire-sdi-secnum-2216",
            datetime.date(2024, 10, 22),
        ),
        (
            "urn:intuitem:risk:library:mapping-ccb-cff-2023-03-01-to-iso27001-2022",
            datetime.date(2024, 11, 4),
        ),
        ("urn:intuitem:risk:library:fedramp-rev5", datetime.date(2024, 5, 8)),
        ("urn:intuitem:risk:library:nist-800-171-rev3", datetime.date(2024, 5, 19)),
        ("urn:intuitem:risk:library:dfs-500-2023-11", datetime.date(2024, 3, 17)),
        (
            "urn:intuitem:risk:library:critical_risk_matrix_5x5",
            datetime.date(2024, 3, 2),
        ),
        ("urn:intuitem:risk:library:lpm-oiv-2019", datetime.date(2024, 3, 30)),
        ("urn:intuitem:risk:library:essential-eight", datetime.date(2024, 3, 17)),
        ("urn:intuitem:risk:library:RNSI-ALGERIE-2020", datetime.date(2024, 11, 3)),
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-der-detektion-und-reaktion",
            datetime.date(2024, 5, 18),
        ),
        ("urn:intuitem:risk:library:nist-csf-1.1", datetime.date(2024, 3, 2)),
        ("urn:intuitem:risk:library:nist-privacy-1.0", datetime.date(2024, 4, 14)),
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-ops-betrieb",
            datetime.date(2024, 5, 18),
        ),
        ("urn:intuitem:risk:library:rts-dora-on-JET", datetime.date(2024, 8, 12)),
        (
            "urn:intuitem:risk:library:esquema-nacional-de-seguridad",
            datetime.date(2024, 8, 20),
        ),
        (
            "urn:intuitem:risk:library:cra-resolution-annexes",
            datetime.date(2024, 6, 25),
        ),
        (
            "urn:intuitem:risk:library:rts-dora-ict-related-incidents",
            datetime.date(2024, 6, 13),
        ),
        (
            "urn:intuitem:risk:library:mapping-cjis-policy-5.9.4-to-cjis-policy-5.9",
            datetime.date(2024, 8, 1),
        ),
        ("urn:intuitem:risk:library:dora", datetime.date(2024, 3, 17)),
        ("urn:intuitem:risk:library:esrs_p3", datetime.date(2024, 9, 9)),
        ("urn:intuitem:risk:library:asf-baseline-v2", datetime.date(2024, 5, 26)),
        ("urn:intuitem:risk:library:pcidss-4_0", datetime.date(2024, 3, 2)),
        ("urn:ackwa:risk:library:mcas-1.0", datetime.date(2024, 5, 17)),
        ("urn:intuitem:risk:library:gl-on-cost-and-losses", datetime.date(2024, 8, 6)),
        (
            "urn:intuitem:risk:library:rts-dora-ict-risk-management",
            datetime.date(2024, 6, 13),
        ),
        (
            "urn:intuitem:risk:library:referentiel-audit-SSI-ANCS-Tunisie",
            datetime.date(2024, 10, 14),
        ),
        (
            "urn:protocolpaladin:risk:library:anssi-recommandations-securite-relatives-tls",
            datetime.date(2024, 8, 4),
        ),
        ("urn:intuitem:risk:library:hds-v2023-a", datetime.date(2024, 4, 6)),
        ("urn:intuitem:risk:library:nist-sp-800-53-rev5", datetime.date(2024, 3, 23)),
        (
            "urn:protocolpaladin:risk:library:mapping-iso27001-2022-to-secnumcloud-3.2",
            datetime.date(2024, 10, 30),
        ),
        (
            "urn:intuitem:risk:library:critical_risk_matrix_3x3",
            datetime.date(2024, 3, 2),
        ),
        ("urn:defend:risk:library:nzism-v3", datetime.date(2024, 9, 18)),
        ("urn:intuitem:risk:library:nist-800-171-rev2", datetime.date(2024, 4, 25)),
        (
            "urn:protocolpaladin:risk:library:anssi-recommandations-configuration-systeme-gnu-linux",
            datetime.date(2024, 5, 12),
        ),
        ("urn:intuitem:risk:library:risk-matrix-3x3-mult", datetime.date(2024, 5, 4)),
        ("urn:intuitem:risk:library:ncsc-caf-3.2", datetime.date(2024, 6, 30)),
        (
            "urn:intuitem:risk:library:map-nist-csf-1.1-iso27001-2022",
            datetime.date(2024, 6, 24),
        ),
        ("urn:ackwa:risk:library:pgssi-s-1.0", datetime.date(2024, 5, 11)),
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-orp-organisation-und-personal",
            datetime.date(2024, 5, 18),
        ),
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-inf-infrastruktur",
            datetime.date(2024, 5, 18),
        ),
        ("urn:intuitem:risk:library:ecc-1", datetime.date(2024, 4, 19)),
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-sys-it-systeme",
            datetime.date(2024, 5, 18),
        ),
        ("urn:intuitem:risk:library:Controlli-Minimi-AGID", datetime.date(2024, 11, 9)),
        (
            "urn:intuitem:risk:library:risk-matrix-6x6-detailed",
            datetime.date(2024, 12, 17),
        ),
        ("urn:intuitem:risk:library:doc-pol", datetime.date(2024, 2, 11)),
        ("urn:intuitem:risk:library:nist-ssdf-1.1", datetime.date(2024, 5, 2)),
        ("urn:intuitem:risk:library:3cf-ed1-v1", datetime.date(2024, 5, 8)),
        ("urn:intuitem:risk:library:ai-act", datetime.date(2024, 5, 29)),
        (
            "urn:intuitem:risk:library:anssi-guide-hygiene-detail",
            datetime.date(2024, 12, 8),
        ),
        ("urn:intuitem:risk:library:cjis-policy-5.9", datetime.date(2024, 7, 31)),
        ("urn:intuitem:risk:library:esrs_p2", datetime.date(2024, 9, 9)),
        ("urn:intuitem:risk:library:ict-minimal", datetime.date(2024, 8, 29)),
        ("urn:intuitem:risk:library:gdpr-checklist", datetime.date(2024, 3, 17)),
        ("urn:intuitem:risk:library:pssi-e", datetime.date(2024, 7, 16)),
        ("urn:intuitem:risk:library:pspf", datetime.date(2024, 2, 11)),
        ("urn:intuitem:risk:library:k_isms_p", datetime.date(2024, 8, 29)),
        ("urn:intuitem:risk:library:iso27001-2013", datetime.date(2024, 7, 4)),
        (
            "urn:intuitem:risk:library:standards-for-safeguarding-customer-information",
            datetime.date(2024, 12, 24),
        ),
        ("urn:intuitem:risk:library:FNCS-v2", datetime.date(2024, 11, 11)),
        ("urn:intuitem:risk:library:cisa-scrm", datetime.date(2024, 9, 14)),
        ("urn:intuitem:risk:library:otcc", datetime.date(2024, 6, 19)),
        ("urn:intuitem:risk:library:gdpr", datetime.date(2024, 7, 12)),
        ("urn:intuitem:risk:library:cmmc-2.0", datetime.date(2024, 3, 2)),
        ("urn:intuitem:risk:library:3cf-v2", datetime.date(2024, 5, 11)),
        (
            "urn:protocolpaladin:risk:library:anssi-recommandations-pour-la-protection-des-sie",
            datetime.date(2024, 6, 10),
        ),
        (
            "urn:intuitem:risk:library:bs-it-gs-2023-isms-sicherheitsmanagement",
            datetime.date(2024, 5, 18),
        ),
        ("urn:intuitem:risk:library:croe-for-fmi", datetime.date(2024, 10, 10)),
        ("urn:intuitem:risk:library:soc2-2017", datetime.date(2024, 3, 2)),
        ("urn:ackwa:risk:library:clausier-sante-v2", datetime.date(2024, 10, 26)),
        (
            "urn:intuitem:risk:library:map-nist-csf-1.1-nist-csf-2.0",
            datetime.date(2024, 6, 29),
        ),
        ("urn:intuitem:risk:library:part-is.d.or", datetime.date(2024, 8, 12)),
        ("urn:intuitem:risk:library:adobe-ccf-v5", datetime.date(2024, 9, 28)),
        ("urn:intuitem:risk:library:nist-csf-2.0", datetime.date(2024, 3, 2)),
        ("urn:intuitem:risk:library:rts-dora-OVS-conduct", datetime.date(2024, 8, 12)),
        ("urn:intuitem:risk:library:tisax-v6.0.2", datetime.date(2024, 4, 15)),
        (
            "urn:ackwa:risk:library:risk-matrix-4x4-pgssi-s-1.0",
            datetime.date(2024, 5, 11),
        ),
        ("urn:intuitem:risk:library:esrs_p1", datetime.date(2024, 9, 9)),
        ("urn:intuitem:risk:library:ccpa_regulations", datetime.date(2024, 7, 3)),
        ("urn:intuitem:risk:library:tiber-eu-2018", datetime.date(2024, 4, 13)),
        ("urn:intuitem:risk:library:cjis-policy-5.9.4", datetime.date(2024, 6, 14)),
        ("urn:intuitem:risk:library:secnumcloud-3.2", datetime.date(2024, 5, 9)),
        (
            "urn:intuitem:risk:library:norea-dora-in-control",
            datetime.date(2024, 11, 10),
        ),
        ("urn:intuitem:risk:library:owasp-asvs-4.0.3", datetime.date(2024, 4, 7)),
        ("urn:intuitem:risk:library:nis1-rules-fr", datetime.date(2024, 7, 29)),
    ]
)


def add_publication_dates(apps, schema_editor):
    StoredLibrary = apps.get_model("core", "StoredLibrary")
    LoadedLibrary = apps.get_model("core", "LoadedLibrary")
    for lib_model in [StoredLibrary, LoadedLibrary]:
        for lib in lib_model.objects.all():
            lib.publication_date = PUBLICATION_DATES.get(lib.urn)
            lib.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0046_riskassessment_ebios_rm_study"),
    ]

    operations = [
        migrations.AddField(
            model_name="loadedlibrary",
            name="publication_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="storedlibrary",
            name="publication_date",
            field=models.DateField(null=True),
        ),
        migrations.RunPython(add_publication_dates),
    ]
