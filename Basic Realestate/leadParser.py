import json
import requests
import pandas as pd
from DataUSA import fetchDataUSData
from Fred import fetchFredData
from news import get_relevant_news
from emailGeneration import generateEmail

LEAD_STATES = []
LEAD_COUNTIES = []
LEAD_COMPANIES = []
STATE_ABBREV_TO_FULL = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming'
}

#functions for leads
def leadsFileToJson(jsonFile):
    try:
        with open(jsonFile, 'r') as file:
            leads = json.load(file)
            return leads
    except FileNotFoundError:
        print("file not there")
    except json.JSONDecodeError:
        print("malformed json")

def parseJson(jsonMessage):
    try:
        parsed = []
        for line in jsonMessage:
            parsed.append(line)
        return parsed
    except FileNotFoundError:
        print("file not there")
    except json.JSONDecodeError:
        print("malformed json")

def breakDownLead(person):
    info = {}
    try:
        for key, value in person.items():
            info[key] = value
        return info
    except json.JSONDecodeError:
        print("malformed json")
        
def load_or_fetch(filepath, fetch_func, **kwargs):
    import os
    if not os.path.exists(filepath):
        data = fetch_func(**kwargs)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print("Saving Data")
    with open(filepath, 'r') as f:
        return json.load(f)
        
def populate_data():
    USAdataframes = {}
    DataUSA = load_or_fetch("dataUSA_data.json", fetchDataUSData, year="2016,2017,2018,2019,2020,2021,2022,2023,2024,2025")
    for name, vals in DataUSA.items():
        df = pd.DataFrame(vals.get("data"), columns=vals.get("columns"))
        if name.endswith('_county') and 'County' in df.columns:
            df['State'] = df['County'].str.split(', ').str[-1]
            df = df[df['State'].isin(LEAD_STATES)]
        USAdataframes[name] = df

    FredDataframes = {}
    DataFred = load_or_fetch("fred_data.json", fetchFredData, states=STATE_ABBREV_TO_FULL.keys())
    for series_id, series_data in DataFred.items():
        observations = series_data.get("observations", [])
        if observations:
            df = pd.DataFrame(observations)
            df['date'] = pd.to_datetime(df['date'])
            df['Year'] = df['date'].dt.year
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            
            if series_id == 'HOUST':
                # Sum for housing starts
                yearly_agg = df.groupby('Year')['value'].sum()
            else:
                # Average for rates (unemployment, mortgage, CPI)
                yearly_agg = df.groupby('Year')['value'].mean()
            
            df_yearly = yearly_agg.reset_index()
            df_yearly.columns = ['Year', 'Value']
            df_yearly['Series'] = series_id
            df_yearly['Units'] = series_data.get("units")
            df_yearly['Title'] = series_data.get("title")
            
            FredDataframes[series_id] = df_yearly
    return USAdataframes, FredDataframes

def DataFormatting(USA, Fred):
    simple_state = {
        'total_population_state': 'Population',
        'tenure_state': 'Household Ownership',
        'median_household_income_state':'Household Income',
        'gini_state': 'Wage GINI',
        'property_value_state': 'Property Value',
        'median_age_state': 'Median Age',
    }
    state_pivots = {}
    for key, value_col in simple_state.items():
        df = USA[key]
        pivot = df.pivot_table(index='State', columns='Year', values=value_col)
        pivot.columns = [f"{value_col}_{yr}" for yr in pivot.columns]
        state_pivots[key] = pivot

    # Merge all simple state pivots into one master state table
    master_state = pd.concat(state_pivots.values(), axis=1)

    renters = USA['renters_by_income_state'].copy()
    cost_burdened = renters[
        ~renters['Gross Rent Percent of Income'].str.contains('Less Than 20|20.0 To 24|25.0 To 29', na=False)
    ]
    renters_pivot = cost_burdened.groupby(['State', 'Year'])['Renters by Income Percentage'].sum()
    renters_pivot = renters_pivot.unstack('Year')
    renters_pivot.columns = [f"Gross_30Percent_Renters_{yr}" for yr in renters_pivot.columns]
    master_state = master_state.join(renters_pivot, how='left')

    # mortgage_costs: just keep "With Mortgage" rows, pivot percentage
    mortgage = USA['mortgage_costs_state'].copy()
    mortgage_with = mortgage[mortgage['Mortgage Status'] == 'With Mortgage']
    mortgage_pivot = mortgage_with.pivot_table(index='State', columns='Year', values='Homeowners by Mortgage')
    mortgage_pivot.columns = [f"Mortgages_Pct_{yr}" for yr in mortgage_pivot.columns]
    master_state = master_state.join(mortgage_pivot, how='left')

    # housing_value_bucket: get median bucket by finding the bucket with most units per state/year
    # (proxy for where the market is concentrated)
    buckets = USA['housing_value_bucket_state'].copy()
    dominant_bucket = (
        buckets.groupby(['State', 'Year', 'Value Bucket'])['Property Value by Bucket']
        .sum()
        .reset_index()
        .sort_values('Property Value by Bucket', ascending=False)
        .groupby(['State', 'Year'])
        .first()
        .reset_index()
        .pivot_table(index='State', columns='Year', values='Value Bucket', aggfunc='first')
    )
    dominant_bucket.columns = [f"Dominant_Value_Bucket_{yr}" for yr in dominant_bucket.columns]
    master_state = master_state.join(dominant_bucket, how='left')

    simple_county = {
        'total_population_county': 'Population',
        'tenure_county': 'Household Ownership',
        'median_household_income_county': 'Household Income',
        'gini_county': 'Wage GINI',
        'property_value_county': 'Property Value',
        'median_age_county': 'Median Age',
    }
    county_pivots = {}
    for key, value_col in simple_county.items():
        if key in USA:
            df = USA[key]
            pivot = df.pivot_table(index=['County'], columns='Year', values=value_col)
            pivot.columns = [f"{value_col}_{yr}" for yr in pivot.columns]
            county_pivots[key] = pivot

    # Merge all county pivots then do same
    master_county = pd.concat(county_pivots.values(), axis=1) if county_pivots else pd.DataFrame()
    if 'renters_by_income_county' in USA:
        renters_county = USA['renters_by_income_county'].copy()
        cost_burdened_county = renters_county[
            ~renters_county['Gross Rent Percent of Income'].str.contains('Less Than 20|20.0 To 24|25.0 To 29', na=False)
        ]
        renters_county_pivot = cost_burdened_county.groupby(['County', 'Year'])['Renters by Income Percentage'].sum()
        renters_county_pivot = renters_county_pivot.unstack('Year')
        renters_county_pivot.columns = [f"Gross_30Percent_Renters_{yr}" for yr in renters_county_pivot.columns]
        master_county = master_county.join(renters_county_pivot, how='left')

    if 'mortgage_costs_county' in USA:
        mortgage_county = USA['mortgage_costs_county'].copy()
        mortgage_county_with = mortgage_county[mortgage_county['Mortgage Status'] == 'With Mortgage']
        mortgage_county_pivot = mortgage_county_with.pivot_table(index=['County'], columns='Year', values='Homeowners by Mortgage')
        mortgage_county_pivot.columns = [f"Mortgages_Pct_{yr}" for yr in mortgage_county_pivot.columns]
        master_county = master_county.join(mortgage_county_pivot, how='left')

    if 'housing_value_bucket_county' in USA:
        buckets_county = USA['housing_value_bucket_county'].copy()
        dominant_bucket_county = (
            buckets_county.groupby(['County', 'Year', 'Value Bucket'])['Property Value by Bucket']
            .sum()
            .reset_index()
            .sort_values('Property Value by Bucket', ascending=False)
            .groupby(['County', 'Year'])
            .first()
            .reset_index()
            .pivot_table(index=['County'], columns='Year', values='Value Bucket', aggfunc='first')
        )
        dominant_bucket_county.columns = [f"Dominant_Value_Bucket_{yr}" for yr in dominant_bucket_county.columns]
        master_county = master_county.join(dominant_bucket_county, how='left')

    fred_national = {}
    fred_state_ur = {}
    for series_id, df in Fred.items():
        if series_id.endswith('UR') and len(series_id) == 4:
            fred_state_ur[series_id] = df
        else:
            fred_national[series_id] = df

    if fred_national:
        fred_national = pd.concat(fred_national.values(), axis=0, ignore_index=True)
    
    if fred_state_ur:
        fred_state_ur = pd.concat(fred_state_ur.values(), axis=0, ignore_index=True)

    if not fred_state_ur.empty:
        ur = fred_state_ur.copy()

        # Extract state abbrev from Series (ALUR -> AL)
        ur['State_Abbr'] = ur['Series'].str.replace('UR', '', regex=False)

        # Map to full state names to match master_state index
        ur['State'] = ur['State_Abbr'].map(STATE_ABBREV_TO_FULL)

        # Pivot to wide format
        ur_pivot = ur.pivot_table(
            index='State',
            columns='Year',
            values='Value'
        )

        # Rename columns
        ur_pivot.columns = [f'Unemployment_{int(c)}' for c in ur_pivot.columns]

        # --- FEATURE 1: Latest unemployment (2026) ---
        if 'Unemployment_2026' in ur_pivot.columns:
            ur_pivot['Unemployment_2026'] = ur_pivot['Unemployment_2026']

        # --- FEATURE 2: 10-year avg excluding COVID years ---
        exclude_years = ['Unemployment_2020', 'Unemployment_2021']
        valid_cols = [
            c for c in ur_pivot.columns
            if c.startswith('Unemployment_') and c not in exclude_years
        ]

        # keep only last ~10 years if more exist
        valid_cols = sorted(valid_cols)[-10:]

        ur_pivot['Unemployment_10yr_Avg_ExCovid'] = ur_pivot[valid_cols].mean(axis=1)

        # Merge into master_state
        master_state = master_state.join(ur_pivot, how='left')

    return master_state, master_county, fred_national

def calculationTime(master_state, master_county):

    def calc_yoy(df, prefix, new_prefix):
        cols = sorted([c for c in df.columns if c.startswith(prefix)])
        years = [int(c.split('_')[-1]) for c in cols]
        for i in range(1, len(cols)):
            prev, curr = cols[i-1], cols[i]
            yr = years[i]
            df[f'{new_prefix}_YOY_{yr}'] = (
                (df[curr] - df[prev]) / df[prev] * 100
            )
        yoy_cols = [c for c in df.columns if c.startswith(f'{new_prefix}_YOY_')]
        if yoy_cols:
            df[f'{new_prefix}_YOY_Avg'] = df[yoy_cols].mean(axis=1)
        return df

    def calc_gini(df):
        gini_cols = sorted([c for c in df.columns if c.startswith('Wage GINI_')])
        if len(gini_cols) >= 2:
            df['GINI_Trend'] = df[gini_cols[-1]] - df[gini_cols[0]]
            df['GINI_Worsening'] = df['GINI_Trend'] > 0
        if gini_cols:
            df['GINI_Avg'] = df[gini_cols].mean(axis=1)
        return df

    def calc_age_score(df):
        age_cols = sorted([c for c in df.columns if c.startswith('Median Age_')])
        for col in age_cols:
            yr = col.split('_')[-1]
            df[f'Age_Score_{yr}'] = (df[col] - 40) * - 1
        age_score_cols = [c for c in df.columns if c.startswith('Age_Score_')]
        if age_score_cols:
            df['Age_Score_Avg'] = df[age_score_cols].mean(axis=1)
        return df

    def calc_ownership_ratio(df):
        ownership_cols = sorted([c for c in df.columns if c.startswith('Household Ownership_')])
        for col in ownership_cols:
            yr = col.split('_')[-1]
            pop_col = f'Population_{yr}'
            if pop_col in df.columns:
                df[f'Ownership_Pop_Ratio_{yr}'] = df[col] / df[pop_col]
        df["Ownership_Pop_Ratio_Avg"] = df[ownership_cols].mean(axis=1)
        return df

    def calc_income_vs_bucket(df):
        bucket_cols = sorted([c for c in df.columns if c.startswith('Dominant_Value_Bucket_')])
        for col in bucket_cols:
            yr = col.split('_')[-1]
            income_col = f'Household Income_{yr}'
            if income_col in df.columns:
                print(master_state[[c for c in master_state.columns if c.startswith('Dominant_Value_Bucket_')]].iloc[0])
                bucket_lower = df[col].str.replace('[$,+]', '', regex=True).str.split('-').str[0].str.strip()

                df[f'Income_vs_Bucket_{yr}'] = df[income_col] - pd.to_numeric(bucket_lower, errors='coerce')
        return df

    def calc_mortgage_trend(df):
        mort_cols = sorted([c for c in df.columns if c.startswith('Mortgages_Pct_')])
        if len(mort_cols) >= 2:
            df['Mortgage_Pct_Trend'] = df[mort_cols[-1]] - df[mort_cols[0]]
            df['Mortgage_Pct_Growing'] = df['Mortgage_Pct_Trend'] > 0
        if mort_cols:
            df['Mortgage_Pct_Avg'] = df[mort_cols].mean(axis=1)
        return df

    def master_calcs(df):
        df = calc_yoy(df, 'Population_', 'Population')
        df = calc_yoy(df, 'Household Income_', 'Income')
        df = calc_yoy(df, 'Property Value_', 'PropVal')
        df = calc_yoy(df, 'Gross_30Percent_Renters_', 'Renters')
        df = calc_gini(df)
        df = calc_age_score(df)
        df = calc_ownership_ratio(df)
        df = calc_mortgage_trend(df)
        return df

    master_state = master_calcs(master_state)
    master_county = master_calcs(master_county)

    return master_state, master_county


STATE_SCORING_METRICS = {
    'Gross_30Percent_Renters_2024': 0.25,
    'Renters_YOY_Avg':              0.20,
    'Population_YOY_Avg':           0.20,
    'Income_YOY_Avg':               0.15,
    'PropVal_YOY_Avg':              0.10,

    'Unemployment_2026':            -0.05,
    'Unemployment_10yr_Avg_ExCovid': -0.05,
}

COUNTY_SCORING_METRICS = {
    'Gross_30Percent_Renters_2024': 0.30,
    'Renters_YOY_Avg':              0.25,
    'Population_YOY_Avg':           0.20,
    'Income_YOY_Avg':               0.15,
    'PropVal_YOY_Avg':              0.10,
}

def scoreMarkets(master_state, master_county, lead_states, lead_counties):
    def z_score_and_rank(df, metrics, is_county=False):
        df = df.copy()
        
        if is_county:
            df = df.reset_index()
            df["State"] = df["County"].str.split(", ").str[-1]
            def score_group(group):
                group = group.copy()

                for col in metrics:
                    mean, std = group[col].mean(), group[col].std()
                    group[f'z_{col}'] = (group[col] - mean) / std if std > 0 else 0

                group['score'] = sum(
                    group[f'z_{col}'].fillna(0) * weight
                    for col, weight in metrics.items()
                )

                group['rank'] = group['score'].rank(ascending=False).astype(int)
                group['total'] = len(group)
                group['percentile'] = ((group['total'] - group['rank']) / group['total'] * 100).round(1)

                return group

            df = df.groupby("State", group_keys=False).apply(score_group)
        else:
            for col in metrics:
                mean, std = df[col].mean(), df[col].std()
                df[f'z_{col}'] = (df[col] - mean) / std if std > 0 else 0

            # weighted score but ignore NaNs
            df['score'] = 0
            for col, weight in metrics.items():
                df['score'] += df[f'z_{col}'].fillna(0) * weight

            df['rank'] = df['score'].rank(ascending=False).astype(int)
            df['total'] = len(df)
            df['percentile'] = ((df['total'] - df['rank']) / df['total'] * 100).round(1)

        return df.sort_values('rank')

    # Score ALL states and ALL counties in the full tables
    all_states_scored = z_score_and_rank(master_state, STATE_SCORING_METRICS)
    all_counties_scored = z_score_and_rank(master_county, COUNTY_SCORING_METRICS, is_county=True)
    print(all_counties_scored)

    lead_state_full = [STATE_ABBREV_TO_FULL[s] for s in lead_states]
    lead_county_names = [county for county, __ in lead_counties]

    scored_leads_states = all_states_scored.loc[
        all_states_scored.index.isin(lead_state_full)
    ]
    scored_leads_counties = all_counties_scored[
        all_counties_scored["County"].isin(lead_county_names)
    ]

    state_display_cols = ['rank', 'total', 'percentile', 'score'] + list(STATE_SCORING_METRICS.keys())
    county_display_cols = ['County', 'rank', 'total', 'percentile', 'score'] + list(COUNTY_SCORING_METRICS.keys())
    print("=== STATE RANKINGS (vs all 50 states) ===")
    print(scored_leads_states[state_display_cols].to_string())
    print()
    print("=== COUNTY RANKINGS (vs all counties in lead states) ===")
    print(scored_leads_counties[county_display_cols].to_string())

    return scored_leads_states, scored_leads_counties

#main
def main():
    people = leadsFileToJson("leads.txt")
    for person in people:
        personalInfo = breakDownLead(person)
        state = personalInfo.get("State").strip()
        county_name = personalInfo.get("PropertyAddress").split(",")[1].strip()
        county = f"{county_name}, {state}"
        name = personalInfo.get("name")
        company = personalInfo.get("Company")

        if personalInfo.get("State") not in LEAD_STATES:
            LEAD_STATES.append(personalInfo.get("State"))
        if (county, state) not in LEAD_COUNTIES:
            LEAD_COUNTIES.append((county, state))
        if (name, company,county_name) not in LEAD_COMPANIES:
            LEAD_COMPANIES.append((name, company, county_name))

    USAdf, Freddf = populate_data()
    master_state, master_county, fred_national= DataFormatting(USAdf, Freddf)
    master_state, master_county = calculationTime(master_state, master_county)
    scored_states, scored_counties = scoreMarkets(master_state, master_county, LEAD_STATES, LEAD_COUNTIES)
    
    final_score = {}
    for county, perc in zip(scored_counties["County"], scored_counties["percentile"]):
        state_name = STATE_ABBREV_TO_FULL[county.split(", ")[-1]]
        state_row = scored_states.loc[state_name]
        state_percentile = state_row["percentile"]
        final_score[county] = round((perc * 0.6) + (state_percentile * 0.4), 2)

    # Convert scored dataframes to dicts for easy lookup
    county_stats = scored_counties.set_index("County").to_dict(orient="index")
    state_stats = scored_states.to_dict(orient="index")

    all_leads_output = []

    for name, company, county_name in LEAD_COMPANIES:
        lead_county = next((c for c, s in LEAD_COUNTIES if c.startswith(county_name)), None)
        lead_state_abbrev = next((s for c, s in LEAD_COUNTIES if c.startswith(county_name)), None)
        lead_state_full = STATE_ABBREV_TO_FULL.get(lead_state_abbrev, "")

        news = get_relevant_news(company_name=company)

        relevant_info = {
            "name": name,
            "company": company,
            "county": lead_county,
            "state": lead_state_full,
            "final_score": final_score.get(lead_county),
            "county_stats": county_stats.get(lead_county, {}),
            "state_stats": state_stats.get(lead_state_full, {}),
            "news": news,
        }

        email = generateEmail(relevant_info)
        relevant_info["email"] = email

        all_leads_output.append(relevant_info)
        print(f"Generated email for {name} at {company}")

    # Dump everything to JSON
    with open("leads_output.json", "w") as f:
        json.dump(all_leads_output, f, indent=2, default=str) 
    print(f"Saved {len(all_leads_output)} leads to leads_output.json")

    df_out = pd.DataFrame(all_leads_output)
    df_out["county_stats"] = df_out["county_stats"].apply(json.dumps, default=str)
    df_out["state_stats"] = df_out["state_stats"].apply(json.dumps, default=str)
    df_out["news"] = df_out["news"].apply(json.dumps)
    df_out.to_csv("leads_output.csv", index=False)
    print(f"Saved {len(all_leads_output)} leads to leads_output.csv")
        

if __name__ == "__main__":
    main()