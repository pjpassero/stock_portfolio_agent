from app.services.reccomend_changes import find_changes


if __name__ == "__main__":

    portfolio = {
        "CVX": 0.23541005210018864,
        "AAPL": 0.09320889930698294,
        "NVDA": 0.06342695040423565,
        "MU": 0.2719763960197438,
        "JPM": 0.10426451851787062,
        "VOO": 0.20619662791952023,
        "VXUS": 0.025516555731458078
    }
    analysis_response = """
                ## Portfolio Summary

                This is an equity-heavy, growth- and sector-concentrated portfolio with strong
                supplied return and risk-adjusted metrics, but meaningful concentration risk in
                a few individual names and sectors.

                The portfolio is fully invested, with no cash allocation. About three-quarters
                is in individual stocks and about one-quarter is in ETFs. The individual stock
                sleeve is the dominant source of portfolio-specific risk, while the ETF sleeve
                provides some diversification but is itself heavily tilted toward U.S.
                large-cap/technology exposure.

                ## Key Takeaways

                ### 1. Strong return profile, but with elevated volatility

                The supplied portfolio return is approximately 34.3%, with portfolio volatility
                of about 24.4%. The Sharpe ratio is 1.24, which indicates that, based on the
                supplied methodology, the portfolio has delivered strong risk-adjusted
                performance.

                That said, the volatility level is meaningful. This is not a low-risk portfolio;
                it behaves like an aggressive equity portfolio, especially because there is no
                cash or fixed income allocation to dampen drawdowns.

                ### 2. Individual stock concentration is the main portfolio risk

                The individual stock sleeve makes up roughly 76.8% of the portfolio. Within
                that sleeve, the concentration is high.

                MU is the largest individual stock exposure. CVX is the second-largest.
                Together, those two holdings represent a little over half of the total portfolio.

                The stock HHI is 0.259, which confirms that the stock sleeve is meaningfully
                concentrated.

                ### 3. Technology exposure is dominant

                The stock sleeve is heavily tilted toward Technology, with Technology
                representing about 55.8% of the individual-stock portion. That comes primarily
                from MU, AAPL, and NVDA.

                The ETF sleeve also has a large Technology allocation, with Technology making
                up about 60.5% of the ETF sector exposure.

                ### 4. Semiconductor exposure is especially important

                Within Technology, the portfolio has a notable semiconductor emphasis through
                MU and NVDA. MU alone is the largest portfolio holding, and NVDA adds another
                layer of exposure to the same broad industry group.

                ### 5. Energy exposure is also large

                Chevron represents about 23.5% of the total portfolio and over 30% of the
                individual-stock sleeve. That is a sizable single-name and sector exposure.

                ### 6. ETF sleeve improves diversification

                The ETF sleeve is about 23.2% of the portfolio. Most of that ETF exposure is in
                VOO, with a much smaller portion in VXUS.

                VOO provides broad U.S. large-cap exposure, while VXUS adds international
                equity exposure.

                ### 7. International exposure is limited

                VXUS represents only a small part of the overall portfolio. International
                diversification exists, but it is not a major driver of portfolio behavior.

                ### 8. No cash or defensive ballast

                The portfolio has 0% cash and no listed fixed income or defensive asset class.

                ## Risk Profile

                Overall, this is an aggressive portfolio. The main risks are:

                - Single-stock concentration risk, especially MU and CVX.
                - Sector concentration risk, especially Technology and Energy.
                - Semiconductor cyclicality, due to MU and NVDA.
                - Equity-only exposure, with no cash or fixed-income cushion.
                - ETF concentration, because the ETF sleeve is heavily dominated by VOO.
                - Limited international diversification, despite having VXUS.

                The supplied portfolio score of 69.8 suggests a portfolio with solid performance
                characteristics but notable risk and diversification weaknesses.

                ## Overall Assessment

                This portfolio has performed well according to the supplied metrics and has a
                strong Sharpe ratio. However, the return profile is being achieved with a high
                level of concentration.

                The core identity of the portfolio is:

                Aggressive, equity-only, U.S.-centric, technology-heavy, with major single-name
                exposure to MU and CVX.

                Potential improvements would involve reducing reliance on a few dominant return
                drivers and broadening diversification across sectors, geographies, or asset
                classes.
                """


changes = find_changes(portfolio, analysis_response)

for change in changes["changes"]:
    print(change["ticker"])

print (find_changes(portfolio, analysis_response))