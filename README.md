# calculation_ordering

This code, when you give it .json files of the form

	{
		"Column 1": "`Column 6` + `Column 5`",
		"Column 2": "8",
	    	"Column 3": "`Column 1`",
		"Column 4": "`Column 2` + 2`",
	    	"Column 5": "`Column 6` *2",
		"Column 6": "`Column 4` + 3"
	}

or 

	{
		"Column D": "100 * `Column C`",
		"Column C": "`Column A` + `Column B`"
	}

Will create an ordering for the columns to be calculated in (as some columns depend on the results of other columns).
