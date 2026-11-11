# Maternal Employment and Self-Rated Mental Health Among U.S. Mothers: Evidence From the 2023–2025 National Survey of Children's Health

*Draft manuscript, v0.2 (November 11, 2026). Detailed analyses, code and tables are documented in the repository (`docs/nsch-h1.md`, `docs/nsch-h1-under2.md`, `docs/nsch-state-policy.md`, `docs/nsch-h8.md`; `src/`; `reports/tables/`).*

## Abstract

Mothers' employment is often discussed as a source of strain, particularly when children are very young, yet evidence on how employment relates to mothers' mental health in the current U.S. context is limited. The current study examined how mothers' self-rated mental health varied by employment status and child age, and tested whether mothers working full-time with a child under 2 reported poorer mental health. Data came from the pooled 2023–2025 National Survey of Children's Health (*n* = 88,047 mothers). Survey-weighted logistic regression accounted for family income, education, marital status, number of children and maternal age. Mothers who were not employed and looking for work were about twice as likely to report fair or poor mental health as mothers employed full-time (12.2%–15.0% vs. 6.7%–7.4%); the gap narrowed after adjustment but remained. Part-time and full-time employed mothers did not differ. Mothers who were out of the labor force resembled full-time employed mothers when their child was 0–5, but reported poorer mental health when their child was older. Full-time employed mothers of children under 2 did not report poorer mental health or more parenting aggravation than other mothers. Part-time and non-employed mothers of children under 2 more often reported that a family member had changed jobs because of child care problems. Practitioners and policymakers should consider the mental health needs of mothers seeking work, and the role of child care access in shaping which mothers remain employed full-time.

*Keywords:* maternal employment, mental health, child care, paid family leave, National Survey of Children's Health

---

## Introduction

Most U.S. mothers are employed, and the question of how paid work relates to their mental health has a long history in psychology and sociology. Two broad perspectives frame this question. Role strain theory holds that the combined demands of work and family can exhaust limited time and energy (Goode, 1960). Role enhancement perspectives argue that holding multiple roles can provide resources, social support and status that outweigh their costs (Barnett & Hyde, 2001; Sieber, 1974). Reviews of this literature have generally found that paid employment does not harm women's mental health on average (Klumb & Lampert, 2004; Repetti et al., 1989), and longitudinal research suggests that continuous employment after a first birth is associated with better midlife health than part-time work, interrupted work or unemployment (Frech & Damaske, 2012).

The period after a birth may be an exception. Returning to work early, or working long hours while an infant is young, has been associated with more depressive symptoms and parenting stress (Chatterji et al., 2013; Mandal, 2018), and the length of maternity leave appears to matter for postpartum mental health (Chatterji & Markowitz, 2005; Dagher et al., 2014). Work–family conflict and the combined load of paid and unpaid work have also been linked to poorer mental health after childbirth (Dagher et al., 2011; Grice et al., 2007). These findings suggest that mothers who work full-time while their child is very young may be at elevated risk for poor mental health.

Policy context may shape these associations. Quasi-experimental evaluations of state paid family leave programs in California and New Jersey have found reductions in parents' psychological distress (Doran et al., 2020; Irish et al., 2021; Lee et al., 2020) and improvements in parents' coping with the day-to-day demands of parenting (Bullinger, 2019), and a recent systematic review concluded that more generous leave is generally associated with better maternal mental health (Heshmati et al., 2023). Access to and the cost of child care also shape whether and how much mothers work (Morrissey, 2017; Ruppanner et al., 2019).

Finally, employment status is not only a potential influence on mental health but also a consequence of it. Poorer health can make it harder to find or keep work (Ross & Mirowsky, 1995), and studies that isolate involuntary job loss suggest that health selection accounts for part of the association between unemployment and mental health (Schmitz, 2011). At the same time, meta-analyses find consistently higher distress among unemployed adults, with larger associations for men than for women (McKee-Ryan et al., 2005; Paul & Moser, 2009).

### The Current Study

The current study used the pooled 2023–2025 National Survey of Children's Health (NSCH) to describe how mothers' self-rated mental health varied by employment status and child age in the United States. The study addressed three aims. First, it examined differences in mothers' mental health across four employment groups (full-time, part-time, not employed and looking for work, and not employed and not looking), before and after accounting for family and socioeconomic characteristics. Second, it tested the hypothesis that mothers employed full-time whose child was under 2 years old would report poorer mental health than (a) other mothers of children under 2 and (b) full-time employed mothers of older children. Third, as exploratory analyses, it examined whether the association differed by state paid family leave policy and between mothers and fathers. All analyses were associational.

## Method

### Data and Participants

The NSCH is an annual, nationally representative address-based survey of U.S. households with children, conducted by the U.S. Census Bureau (U.S. Census Bureau, 2025a, 2025b, 2026c). One child is sampled per household, and an adult who knows about the child's health completes the questionnaire. The 2023, 2024 and 2025 topical public use files were pooled, as recommended for subgroup estimates (U.S. Census Bureau, 2025d).

Mothers were defined as respondents (Adult 1) who were female and the sampled child's biological or adoptive parent (90,415 mothers). Mothers whose employment was "working without pay" (*n* = 1,361) or missing (*n* = 821), or whose mental health rating was missing (*n* = 186), were excluded, leaving an analytic sample of 88,047 mothers. Regression models additionally excluded mothers missing marital status, age or physical health (final model sample *n* = 87,318). Because NSCH weights describe children, estimates are interpreted as the percentage of children whose mother reported a given characteristic (U.S. Census Bureau, 2026a). Table 1 describes the sample.

### Measures

**Mental health.** Mothers rated their own mental or emotional health as excellent, very good, good, fair or poor (`A1_MENTHEALTH`). The main outcome was a fair or poor rating. Single-item self-rated mental health correlates moderately with multi-item measures of distress and depression (Ahmad et al., 2014; Fleishman & Zuvekas, 2007), but it is not a diagnostic measure. In the analyses of children under 2, the full 1–5 rating was also analyzed as a mean score and at each cut-off of the scale.

**Parenting strain.** Parenting aggravation was coded as reporting "usually" or "always" during the past month on at least one of three items: the child is much harder to care for than most children their age (`K8Q31`), the child does things that really bother the parent a lot (`K8Q32`), and feeling angry with the child (`K8Q34`). Mothers also reported how well they were handling the day-to-day demands of raising children (`K8Q30`); "not very well" or "not well at all" was coded as not handling demands.

**Child care–related job change.** For children aged 0–5, respondents reported whether anyone in the family had to quit, not take, or greatly change a job because of problems with child care in the past 12 months (`K6Q27`).

**Employment.** Mothers reported their current employment status (`A1_EMPLOYED_R`), grouped as employed full-time, employed part-time, not employed and looking for work, and not employed and not looking for work. Retired mothers (*n* = 882) were combined with the not-looking group; excluding them changed estimates by at most 0.3 percentage points. NSCH does not measure work hours.

**Child age.** Child age was the sampled child's age in years, grouped as 0–5, 6–11 and 12–17. For the second aim, children under 2 (ages 0–1) were compared with older children, with ages 0–2 as a sensitivity analysis.

**Covariates.** Covariates were family income as a percentage of the federal poverty level (FPL; <100%, 100%–199%, 200%–399%, ≥400%), maternal education, marital status, number of children in the household, maternal age and survey year. Income is multiply imputed in the NSCH for about one fifth of families, so all models were estimated on each of the six imputations and combined using Rubin's rules (Rubin, 1987; U.S. Census Bureau, 2025c).

**State paid family leave.** For exploratory analyses, states were coded as having paid family leave if a mandatory state program paid bonding benefits by the child's birth month (California, Connecticut, District of Columbia, Massachusetts, New Jersey, New York, Rhode Island and Washington in all years; Oregon from September 2023; Colorado from January 2024). Program dates came from official state program websites and a national compilation (National Partnership for Women & Families, 2026).

### Analytic Strategy

All estimates used the NSCH child weights divided by the number of pooled years, with design-based standard errors from Taylor linearization (strata defined by survey year, state and sampling stratum; households as primary sampling units) and mothers estimated as a domain of the full sample (Binder, 1983; Lumley, 2004; U.S. Census Bureau, 2026a). Estimates were checked against the NSCH reliability criteria: an unweighted denominator of at least 30, and a 95% confidence interval no wider than 20 percentage points or 1.2 times the estimate (U.S. Census Bureau, 2026b).

For the first aim, descriptive percentages were followed by survey-weighted logistic regression. Model 0 included employment, child age band and survey year. Model 1, the main model, added income, education, marital status, number of children and maternal age. Model 2 added maternal physical health as a sensitivity analysis, because physical health may be either a cause or a consequence of both employment and mental health. Results are reported as adjusted percentages (predictive margins) and percentage-point differences from full-time employment. An employment × child age interaction tested whether the differences varied by child age. An exploratory Fairlie (2005) decomposition estimated how much of each unadjusted gap was accounted for by group differences in the Model 1 covariates.

For the second aim, the same approach compared full-time employed mothers of children under 2 with other mothers of children under 2, and with full-time employed mothers of older children. For the exploratory aims, models were estimated separately within paid-leave and other states (with standard errors clustered by state) and separately for mothers and fathers, and differences between the employment gaps were estimated.

## Results

### Sample Characteristics

As shown in Table 1, mothers who were not employed and looking for work more often had low family incomes, a high school education or less, and were less often married than full-time employed mothers. Mothers not looking for work were the most likely to be married and to have three or more children.

**Table 1**

*Characteristics of Mothers by Employment Status, NSCH 2023–2025*

| Characteristic | All mothers | Full-time | Part-time | Not employed, looking | Not employed, not looking |
|---|---|---|---|---|---|
| Unweighted *n* | 87,520 | 55,664 | 14,265 | 4,335 | 13,256 |
| Child age 0–5 | 30.8 | 28.4 | 31.1 | 32.8 | 37.0 |
| Child age 6–11 | 33.7 | 33.5 | 34.5 | 36.4 | 32.4 |
| Child age 12–17 | 35.5 | 38.1 | 34.4 | 30.9 | 30.6 |
| Mother aged 18–34 | 24.3 | 19.8 | 26.6 | 35.4 | 31.4 |
| Married | 71.4 | 70.4 | 72.3 | 51.3 | 82.8 |
| Never married | 9.0 | 8.9 | 9.0 | 19.2 | 4.7 |
| High school or less | 25.4 | 17.2 | 27.3 | 52.4 | 36.8 |
| Bachelor's degree or higher | 49.3 | 58.5 | 45.6 | 20.5 | 37.3 |
| Three or more children | 34.1 | 27.2 | 37.2 | 42.2 | 49.2 |
| Income below 100% FPL | 17.6 | 10.0 | 21.5 | 48.6 | 23.5 |
| Income 400% FPL or more | 32.8 | 41.0 | 26.3 | 10.7 | 23.6 |

*Note.* Values are weighted column percentages unless noted. Sample: mothers with employment, mental health, marital status and age reported. Income categories are averaged across the six imputations. FPL = federal poverty level. Full rows in `reports/tables/manuscript/table1_characteristics.csv`.

### Aim 1: Employment Status and Mental Health

Children whose mothers were not employed and looking for work were about twice as likely as children whose mothers worked full-time to have a mother who rated her mental health as fair or poor, in every child age band (Table 2). Part-time and full-time employed mothers did not differ in any band. Mothers not looking for work resembled full-time employed mothers when the child was 0–5 (7.5% vs. 7.4%), but reported more fair or poor mental health when the child was 12–17 (12.1% vs. 6.7%). No estimate failed the NSCH reliability criteria.

**Table 2**

*Percentage of Children Whose Mother Rated Her Mental Health as Fair or Poor, by Mother's Employment and Child Age*

| Mother's employment | Child 0–5 | Child 6–11 | Child 12–17 |
|---|---|---|---|
| Full-time | 7.4 [6.6, 8.3] | 6.7 [5.9, 7.7] | 6.7 [6.1, 7.4] |
| Part-time | 8.4 [7.0, 10.0] | 7.6 [6.2, 9.2] | 6.9 [5.8, 8.1] |
| Not employed, looking | 15.0 [11.8, 19.0] | 13.8 [11.2, 16.9] | 12.2 [9.9, 15.0] |
| Not employed, not looking | 7.5 [6.3, 9.0] | 9.4 [7.6, 11.7] | 12.1 [9.6, 15.1] |

*Note.* Weighted percentages with 95% confidence intervals (logit-transformed) in brackets. *n* = 88,047 mothers.

After adjustment for income, education, marital status, number of children and maternal age (Model 1), the difference between mothers looking for work and full-time employed mothers narrowed from 6.7 to 3.0 percentage points, 95% CI [1.5, 4.5], but remained (Table 3). The difference for mothers not looking for work did not narrow (2.5 to 2.7 points, 95% CI [1.3, 4.1]). Adding physical health (Model 2) reduced both differences (1.8 and 1.1 points). Part-time employed mothers did not differ from full-time employed mothers in any model.

**Table 3**

*Adjusted Differences in Fair or Poor Mental Health Compared With Full-Time Employed Mothers*

| Mother's employment | Model 0 | Model 1 | Model 2 |
|---|---|---|---|
| Part-time | 0.6 [−0.4, 1.5] | 0.0 [−0.9, 0.9] | 0.2 [−0.7, 1.1] |
| Not employed, looking | 6.7 [4.9, 8.5] | 3.0 [1.5, 4.5] | 1.8 [0.4, 3.2] |
| Not employed, not looking | 2.5 [1.2, 3.8] | 2.7 [1.3, 4.1] | 1.1 [0.0, 2.3] |

*Note.* Percentage-point differences in predicted probabilities with 95% confidence intervals in brackets. Model 0: child age band and survey year. Model 1: Model 0 plus income, education, marital status, number of children and maternal age. Model 2: Model 1 plus physical health. *n* = 87,318.

The employment × child age interaction was significant, χ²(6) = 20.2, *p* = .003. In Model 1, the difference between mothers not looking for work and full-time employed mothers was −0.4 points (95% CI [−2.1, 1.3]) when the child was 0–5, 2.9 points (95% CI [0.5, 5.2]) when the child was 6–11 and 6.1 points (95% CI [3.2, 8.9]) when the child was 12–17. The difference for mothers looking for work was similar across age bands (2.2–3.7 points).

In the exploratory decomposition, differences in the Model 1 covariates accounted for 2.7 of the 6.7-point unadjusted gap between mothers looking for work and full-time employed mothers (41%), mainly marital status, maternal age and income. For mothers not looking for work, covariate differences accounted for almost none of the gap: their lower income and education would have widened it, but their higher rate of marriage would have narrowed it.

### Aim 2: Full-Time Employed Mothers of Children Under 2

The hypothesis was not supported. Among mothers of children under 2, full-time employed mothers did not report poorer mental health than part-time or non-employed mothers on any outcome (Table 4). After adjustment, 7.4% of full-time employed mothers of children under 2 reported fair or poor mental health, compared with 6.0% of part-time employed mothers and 8.5% of mothers not looking for work; none of the differences was statistically significant. The same pattern held for the mean rating, each cut-off of the rating scale and when children under 3 were analyzed. For parenting aggravation, the only significant difference ran opposite to the hypothesis: part-time employed mothers reported more aggravation than full-time employed mothers (4.0% vs. 1.5%), although this estimate did not meet the NSCH reliability criteria.

Among full-time employed mothers, those whose child was under 2 reported slightly better mental health than those with older children. Compared with mothers of children under 2, mothers of children aged 2–5, 6–11 and 12–17 had higher (worse) adjusted mean ratings (by 0.11, 0.08 and 0.09 points on the 1–5 scale) and were 3.5–4.3 points more likely to rate their mental health as good, fair or poor. They were also 2.8–4.2 points more likely to report parenting aggravation.

The clearest difference among mothers of children under 2 concerned child care. After adjustment, 7.8% of full-time employed mothers reported a child care–related job change in the family, compared with 22.6% of part-time employed mothers, 30.1% of mothers looking for work and 15.1% of mothers not looking for work.

**Table 4**

*Outcomes Among Mothers of Children Under 2, by Mother's Employment (Adjusted)*

| Outcome | Full-time | Part-time | Not employed, looking | Not employed, not looking |
|---|---|---|---|---|
| Unweighted *n* | 3,753 | 1,108 | 357 | 1,500 |
| Mental health rating, mean (1–5) | 2.13 | 2.12 | 2.31 | 2.17 |
| Fair or poor mental health (%) | 7.4 | 6.0 | 10.5 | 8.5 |
| Good, fair or poor mental health (%) | 32.7 | 30.0 | 41.4 | 34.2 |
| Parenting aggravation (%) | 1.5 | 4.0<sup>a</sup>\* | 3.9<sup>a</sup> | 2.1 |
| Child care–related job change (%) | 7.8 | 22.6\* | 30.1\* | 15.1\* |

*Note.* Adjusted for survey year, income, education, marital status, number of children and maternal age. Higher values indicate worse outcomes. Mean ratings and percentages are predictive margins. *n* for each outcome differs slightly because of item nonresponse.
<sup>a</sup> Estimate flagged under the NSCH reliability criteria.
\* Difference from full-time employed mothers, 95% CI excludes zero.

### Exploratory Analyses

**State paid family leave.** In both paid-leave states and other states, full-time employed mothers of children under 2 did not report poorer mental health than other mothers. The difference between full-time and non-employed mothers was −1.1 points (95% CI [−2.8, 0.7]) in states without paid leave and −3.7 points (95% CI [−11.1, 3.8]) in paid-leave states; the difference between these gaps was not significant (−2.6 points, 95% CI [−9.7, 4.4]). With about 690 full-time employed mothers of children under 2 in paid-leave states, this comparison could not rule out moderate differences.

**Fathers.** The difference in fair or poor mental health between non-employed and full-time employed fathers (6.7 points, 95% CI [4.4, 8.9]) was more than twice that among mothers (2.8 points, 95% CI [1.7, 3.9]); the difference between them was −3.8 points, 95% CI [−6.3, −1.3]. Full-time employed fathers reported fair or poor mental health about half as often as full-time employed mothers (3.4%–4.4% vs. 6.7%–7.4%).

## Discussion

The current study examined how mothers' self-rated mental health varied by employment status and child age in a large, recent, nationally representative sample. Three patterns emerged. First, mothers who were looking for work reported poorer mental health than employed mothers, consistent with research on unemployment and distress (Paul & Moser, 2009) and on mothers' work pathways after childbirth (Frech & Damaske, 2012). About 40% of this gap was accounted for by differences in marital status, age and income, but the remainder was not explained by measured characteristics. Because poorer mental health can also make work harder to find (Ross & Mirowsky, 1995; Schmitz, 2011), this association likely reflects influences in both directions.

Second, part-time and full-time employed mothers did not differ, in line with studies finding few mental health differences between these groups (Buehler & O'Brien, 2011). Third, mothers out of the labor force resembled employed mothers while their children were young, but reported poorer mental health when their children were older. One interpretation is that staying home with a young child is a common, often chosen arrangement, whereas being out of the labor force with an older child more often coincides with health problems or caregiving demands (Schieve et al., 2011; Thomas et al., 2005). The current data cannot distinguish these explanations.

Contrary to the hypothesis, full-time employed mothers of children under 2 did not report poorer mental health or more parenting strain than other mothers, and reported slightly better mental health than full-time employed mothers of older children. This finding is consistent with reviews concluding that paid work does not harm women's mental health (Klumb & Lampert, 2004) and with evidence that returning to work is associated with fewer depressive symptoms after childbirth (Mandal, 2018). It differs from findings that longer work hours at 6 months postpartum are associated with more depressive symptoms (Chatterji et al., 2013). That study measured work hours and depressive symptoms within a narrow postpartum window, whereas the NSCH measures only employment status, a single global mental health rating and child age in years.

The child care findings offer one explanation for the null result. Mothers of children under 2 who worked part-time or were not employed were two to four times as likely as full-time employed mothers to report a child care–related job change in the family. Mothers for whom full-time work with an infant was not sustainable may already have reduced their hours or left work, leaving a full-time employed group for whom work and child care fit together. Such selection would mask strain associated with full-time employment in cross-sectional data, and is consistent with evidence that child care costs and leave policies shape mothers' employment (Morrissey, 2017; Rossin-Slater et al., 2013).

### Limitations and Future Directions

Several limitations should be considered. First, the data are cross-sectional, so the direction of associations cannot be determined, and selection into employment may account for part of every comparison. Second, mental health was measured with a single global self-rating, which is less sensitive than validated depression and anxiety scales (Fleishman & Zuvekas, 2007) and does not capture postpartum depression or anxiety specifically. Third, the NSCH does not measure work hours, schedules, job quality, leave taken or the timing of the return to work. Fourth, the sample includes only mothers who completed the survey; about one third of identified mothers appeared only as a second adult and were excluded. Fifth, "under 2" refers to the sampled child, so mothers with an infant and an older sampled child were classified by the older child. Finally, some groups were small (e.g., 357 mothers of children under 2 who were looking for work), and the state paid family leave comparison was underpowered.

Future research should test the hypothesis with validated mental health measures and work hours. The National Health Interview Survey includes the PHQ-8 and GAD-7 in selected years, links parents to sampled children, and records weekly work hours, making it the most practical public source for this purpose. Time-use data from the American Time Use Survey could examine whether full-time employed mothers of infants differ in sleep and total workload, factors linked to postpartum depressive symptoms (Dagher et al., 2011). Longitudinal data would be needed to separate the effects of employment from selection into employment.

### Conclusions

In a nationally representative sample of U.S. mothers, being out of work while looking for work was associated with poorer self-rated mental health, whereas full-time employment, including with a child under 2, was not. Child care problems were concentrated among mothers of young children who were not employed full-time. Practitioners and policymakers should consider the mental health needs of mothers seeking work, and the role of child care access in determining which mothers are able to remain employed.

---

## References

Ahmad, F., Jhajj, A. K., Stewart, D. E., Burghardt, M., & Bierman, A. S. (2014). Single item measures of self-rated mental health: A scoping review. *BMC Health Services Research, 14*, Article 398. https://doi.org/10.1186/1472-6963-14-398

Barnett, R. C., & Hyde, J. S. (2001). Women, men, work, and family: An expansionist theory. *American Psychologist, 56*(10), 781–796. https://doi.org/10.1037/0003-066X.56.10.781

Binder, D. A. (1983). On the variances of asymptotically normal estimators from complex surveys. *International Statistical Review, 51*(3), 279–292. https://doi.org/10.2307/1402588

Buehler, C., & O'Brien, M. (2011). Mothers' part-time employment: Associations with mother and family well-being. *Journal of Family Psychology, 25*(6), 895–906. https://doi.org/10.1037/a0025993

Bullinger, L. R. (2019). The effect of paid family leave on infant and parental health in the United States. *Journal of Health Economics, 66*, 101–116. https://doi.org/10.1016/j.jhealeco.2019.05.006

Chatterji, P., & Markowitz, S. (2005). Does the length of maternity leave affect maternal health? *Southern Economic Journal, 72*(1), 16–[VERIFY end page]. https://doi.org/10.2307/20062092

Chatterji, P., Markowitz, S., & Brooks-Gunn, J. (2013). Effects of early maternal employment on maternal health and well-being. *Journal of Population Economics, 26*(1), 285–301. https://doi.org/10.1007/s00148-012-0437-5

Dagher, R. K., McGovern, P. M., & Dowd, B. E. (2014). Maternity leave duration and postpartum mental and physical health: Implications for leave policies. *Journal of Health Politics, Policy and Law, 39*(2), 369–416. https://doi.org/10.1215/03616878-2416247

Dagher, R. K., McGovern, P. M., Dowd, B. E., & Lundberg, U. (2011). Postpartum depressive symptoms and the combined load of paid and unpaid work: A longitudinal analysis. *International Archives of Occupational and Environmental Health, 84*(7), 735–743. https://doi.org/10.1007/s00420-011-0626-7

Doran, E. L., Bartel, A. P., Ruhm, C. J., & Waldfogel, J. (2020). California's paid family leave law improves maternal psychological health. *Social Science & Medicine, 256*, Article 113003. https://doi.org/10.1016/j.socscimed.2020.113003

Fairlie, R. W. (2005). An extension of the Blinder–Oaxaca decomposition technique to logit and probit models. *Journal of Economic and Social Measurement, 30*(4), 305–316. https://doi.org/10.3233/JEM-2005-0259

Fleishman, J. A., & Zuvekas, S. H. (2007). Global self-rated mental health: Associations with other mental health measures and with role functioning. *Medical Care, 45*(7), 602–609. https://doi.org/10.1097/MLR.0b013e31803bb4b0

Frech, A., & Damaske, S. (2012). The relationships between mothers' work pathways and physical and mental health. *Journal of Health and Social Behavior, 53*(4), 396–412. https://doi.org/10.1177/0022146512453929

Goode, W. J. (1960). A theory of role strain. *American Sociological Review, 25*(4), 483–[VERIFY end page]. https://doi.org/10.2307/2092933

Grice, M. M., Feda, D., McGovern, P., Alexander, B. H., McCaffrey, D., & Ukestad, L. (2007). Giving birth and returning to work: The impact of work–family conflict on women's health after childbirth. *Annals of Epidemiology, 17*(10), 791–798. https://doi.org/10.1016/j.annepidem.2007.05.002

Heshmati, A., Honkaniemi, H., & Juárez, S. P. (2023). The effect of parental leave on parents' mental health: A systematic review. *The Lancet Public Health, 8*(1), e57–e75. https://doi.org/10.1016/S2468-2667(22)00311-5

Irish, A. M., White, J. S., Modrek, S., & Hamad, R. (2021). Paid family leave and mental health in the U.S.: A quasi-experimental study of state policies. *American Journal of Preventive Medicine, 61*(2), 182–191. https://doi.org/10.1016/j.amepre.2021.03.018

Klumb, P. L., & Lampert, T. (2004). Women, work, and well-being 1950–2000: A review and methodological critique. *Social Science & Medicine, 58*(6), 1007–1024. https://doi.org/10.1016/S0277-9536(03)00262-4

Lee, B. C., Modrek, S., White, J. S., Batra, A., Collin, D. F., & Hamad, R. (2020). The effect of California's paid family leave policy on parent health: A quasi-experimental study. *Social Science & Medicine, 251*, Article 112915. https://doi.org/10.1016/j.socscimed.2020.112915

Lumley, T. (2004). Analysis of complex survey samples. *Journal of Statistical Software, 9*(8). https://doi.org/10.18637/jss.v009.i08

Mandal, B. (2018). The effect of paid leave on maternal mental health. *Maternal and Child Health Journal, 22*(10), 1470–1476. https://doi.org/10.1007/s10995-018-2542-x

McKee-Ryan, F., Song, Z., Wanberg, C. R., & Kinicki, A. J. (2005). Psychological and physical well-being during unemployment: A meta-analytic study. *Journal of Applied Psychology, 90*(1), 53–76. https://doi.org/10.1037/0021-9010.90.1.53

Morrissey, T. W. (2017). Child care and parent labor force participation: A review of the research literature. *Review of Economics of the Household, 15*(1), 1–24. https://doi.org/10.1007/s11150-016-9331-3

National Partnership for Women & Families. (2026, April). *State paid family & medical leave insurance laws*. https://nationalpartnership.org/our-work/resources/economic-justice/paid-leave/state-paid-family-leave-laws.pdf

Paul, K. I., & Moser, K. (2009). Unemployment impairs mental health: Meta-analyses. *Journal of Vocational Behavior, 74*(3), 264–282. https://doi.org/10.1016/j.jvb.2009.01.001

Repetti, R. L., Matthews, K. A., & Waldron, I. (1989). Employment and women's health: Effects of paid employment on women's mental and physical health. *American Psychologist, 44*(11), 1394–1401. https://doi.org/10.1037/0003-066X.44.11.1394

Ross, C. E., & Mirowsky, J. (1995). Does employment affect health? *Journal of Health and Social Behavior, 36*(3), 230–243. https://doi.org/10.2307/2137340

Rossin-Slater, M., Ruhm, C. J., & Waldfogel, J. (2013). The effects of California's paid family leave program on mothers' leave-taking and subsequent labor market outcomes. *Journal of Policy Analysis and Management, 32*(2), 224–245. https://doi.org/10.1002/pam.21676

Rubin, D. B. (1987). *Multiple imputation for nonresponse in surveys*. John Wiley & Sons. https://doi.org/10.1002/9780470316696

Ruppanner, L., Moller, S., & Sayer, L. (2019). Expensive childcare and short school days = lower maternal employment and more time in childcare? Evidence from the American Time Use Survey. *Socius, 5*. https://doi.org/10.1177/2378023119860277

Schieve, L. A., Boulet, S. L., Kogan, M. D., Yeargin-Allsopp, M., Boyle, C. A., Visser, S. N., Blumberg, S. J., & Rice, C. (2011). Parenting aggravation and autism spectrum disorders: 2007 National Survey of Children's Health. *Disability and Health Journal, 4*(3), 143–152. https://doi.org/10.1016/j.dhjo.2010.09.002

Schmitz, H. (2011). Why are the unemployed in worse health? The causal effect of unemployment on health. *Labour Economics, 18*(1), 71–78. https://doi.org/10.1016/j.labeco.2010.08.005

Sieber, S. D. (1974). Toward a theory of role accumulation. *American Sociological Review, 39*(4), 567–[VERIFY end page]. https://doi.org/10.2307/2094422

Thomas, C., Benzeval, M., & Stansfeld, S. A. (2005). Employment transitions and mental health: An analysis from the British household panel survey. *Journal of Epidemiology and Community Health, 59*(3), 243–249. https://doi.org/10.1136/jech.2004.019778

U.S. Census Bureau. (2025a). *2023 National Survey of Children's Health: Topical public use file (enhanced), Stata format* [Data set]. https://www2.census.gov/programs-surveys/nsch/datasets/2023/nsch_2023e_topical_Stata.zip

U.S. Census Bureau. (2025b). *2024 National Survey of Children's Health: Topical public use file, Stata format* [Data set]. https://www2.census.gov/programs-surveys/nsch/datasets/2024/nsch_2024_topical_Stata.zip

U.S. Census Bureau. (2025c, October 6). *National Survey of Children's Health: Analysis with multiply imputed data*. https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/NSCH-Analysis-with-Imputed-Data-Guide.pdf

U.S. Census Bureau. (2025d, October 6). *National Survey of Children's Health: Guide to multi-year estimates*. https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/NSCH-Guide-to-Multi-Year-Estimates.pdf

U.S. Census Bureau. (2026a, October 1). *2025 National Survey of Children's Health: Comprehensive analytic guide*. https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/NSCH-Analytic-Guide.pdf

U.S. Census Bureau. (2026b, October 1). *2025 National Survey of Children's Health: Methodology report*. https://www2.census.gov/programs-surveys/nsch/technical-documentation/methodology/2025-NSCH-Methodology-Report.pdf

U.S. Census Bureau. (2026c). *2025 National Survey of Children's Health: Topical public use file (enhanced), Stata format* [Data set]. https://www2.census.gov/programs-surveys/nsch/datasets/2025/nsch_2025_topical_Stata.zip
