public class Loan
{
    public string AgeRange { get; set; }
    public string City { get; set; }
    public decimal InterestRate { get; set; }
    // Inne właściwości potrzebne do wygenerowania raportu.
}

public interface IFinancialReportStrategy
{
    Func<Loan, bool> GetPredicate();
    IEnumerable<Tuple<string, string, decimal>> GetMetrics(Func<Loan, bool> predicate);
    IEnumerable<Tuple<decimal, string>> GetStatistics(Func<Loan, bool> predicate);
}

public class FirstBankFinancialReportStrategy : IFinancialReportStrategy
{
    public Func<Loan, bool> GetPredicate()
    {
        return loan => /* Warunek dla Banku A. */;
    }

    public IEnumerable<Tuple<string, string, decimal>> GetMetrics(Func<Loan, bool> predicate)
    {
        // Tutaj wprowadź implementację dla Banku A.
    }

    public IEnumerable<Tuple<decimal, string>> GetStatistics(Func<Loan, bool> predicate)
    {
        // Tutaj wprowadź implementację dla Banku A.
    }
}

public class SecondBankFinancialReportStrategy : IFinancialReportStrategy
{
    public Func<Loan, bool> GetPredicate()
    {
        return loan => /* Warunek dla Banku B. */;
    }

    public IEnumerable<Tuple<string, string, decimal>> GetMetrics(Func<Loan, bool> predicate)
    {
        // Tutaj wprowadź implementację dla Banku B.
    }

    public IEnumerable<Tuple<decimal, string>> GetStatistics(Func<Loan, bool> predicate)
    {
        // Tutaj wprowadź implementację dla Banku B.
    }
}

public class FinancialReport
{
    private readonly IFinancialReportStrategy _strategy;

    public FinancialReport(IFinancialReportStrategy strategy)
    {
        _strategy = strategy;
    }

    public IEnumerable<Tuple<string, string, decimal>> GetMetrics()
    {
        var predicate = _strategy.GetPredicate();
        return _strategy.GetMetrics(predicate);
    }

    public IEnumerable<Tuple<decimal, string>> GetStatistics()
    {
        var predicate = _strategy.GetPredicate();
        return _strategy.GetStatistics(predicate);
    }
}
FinancialReport firstFinancialStrategy = new FinancialReport(new FirstBankFinancialReportStrategy());

var firstMetrics = firstFinancialStrategy.GetMetrics();

Assert.AreEqual(3, firstMetrics.Count(m => m.Item2 == "Kraków"));
Assert.AreEqual(3, firstMetrics.Count(m => m.Item2 == "Warszawa"));
Assert.AreEqual(3, firstMetrics.Count(m => m.Item2 == "Gdańsk"));

FinancialReport secondFinancialStrategy = new FinancialReport(new SecondBankFinancialReportStrategy());

var secondMetrics = secondFinancialStrategy.GetMetrics();
var secondStatistics = secondFinancialStrategy.GetStatistics();

Assert.AreEqual(9, secondMetrics.Count());
Assert.AreEqual(9, secondStatistics.Count());

FinancialReport firstFinancialStrategy = new FinancialReport(new FirstBankFinancialReportStrategy());

var firstMetrics = firstFinancialStrategy.GetMetrics();

Assert.AreEqual("18-30", firstMetrics.Where(m => m.Item2 == "Kraków").OrderBy(m => m.Item3).First().Item1);
Assert.AreEqual("31-50", firstMetrics.Where(m => m.Item2 == "Warszawa").OrderByDescending(m => m.Item3).First().Item1);
Assert.AreEqual(0.12M, firstMetrics.Where(m => m.Item2 == "Gdańsk" && m.Item1 == "51-70").First().Item3);


