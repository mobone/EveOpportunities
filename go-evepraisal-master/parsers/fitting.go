package main
import "C"
import (
	"fmt"
	"regexp"
	"sort"
	"strings"
	"strconv"
)


type Input map[int]string
//export Add
type ParserResult interface {
	// Name is the name of the PARSER that yielded this result
	Name() string
	Lines() []int
}
//export Add
var bigNumberRegex = `[\d,'\.\ ’` + "\u00a0\xc2\xa0’" + `]`
var cleanIntegers = regexp.MustCompile(`[,\'\.\ ’` + "\u00a0\xc2\xa0" + `]`)
var separatorCharacters = map[rune]bool{
	',':    true,
	'.':    true,
	' ':    true,
	'\'':   true,
	'\xc2': true,
	'\xa0': true,
	'’':    true,
}
//export splitDecimal
func splitDecimal(s string) (string, string) {
	runes := []rune(s)
	if len(runes) > 3 {
		_, twodecimal := separatorCharacters[runes[len(runes)-3]]
		if twodecimal {
			whole := string(runes[0 : len(runes)-3])
			decimal := string(runes[len(runes)-2:])
			return whole, decimal
		}
	}
	if len(runes) > 2 {
		_, onedecimal := separatorCharacters[runes[len(runes)-2]]
		if onedecimal {
			whole := string(runes[0 : len(runes)-2])
			decimal := string(runes[len(runes)-1:])
			return whole, decimal
		}
	}

	return s, ""
}

// ToInt parses a string into an integer. It will return 0 on failure
func ToInt(s string) int64 {
	if s == "" {
		return 0
	}

	whole, _ := splitDecimal(s)
	cleaned := cleanIntegers.ReplaceAllString(whole, "")

	i, err := strconv.ParseInt(cleaned, 10, 64)
	if err == nil {
		return i
	}

	return 0
}

// ToFloat64 parses a string into a float64. It will return 0.0 on failure
func ToFloat64(s string) float64 {
	// Attempt to parse float as "normal"
	f, err := strconv.ParseFloat(s, 64)
	if err == nil {
		return f
	}

	whole, decimal := splitDecimal(s)
	f, _ = strconv.ParseFloat(fmt.Sprintf("%d.%s", ToInt(string(whole)), string(decimal)), 64)

	return f
}

// CleanTypeName will remove leading and trailing whitespace and leading asterisks.
func CleanTypeName(s string) string {
	return strings.TrimSuffix(strings.Trim(s, " "), "*")
}

func regexMatchedLines(matches map[int][]string) []int {
	keys := make([]int, len(matches))
	i := 0
	for k := range matches {
		keys[i] = k
		i++
	}
	sort.Ints(keys)
	return keys
}

func regexParseLines(re *regexp.Regexp, input Input) (map[int][]string, Input) {
	matches := make(map[int][]string)
	rest := make(Input)
	for i, line := range input {
		match := re.FindStringSubmatch(line)
		if len(match) == 0 {
			rest[i] = line
		} else {
			matches[i] = match
		}
	}
	return matches, rest
}

func StringsToInput(lines []string) Input {
	m := make(Input)
	for i, line := range lines {
		m[i] = line
	}
	return m
}

func StringToInput(s string) Input {
	s = strings.Replace(s, "\r", "", -1)
	return StringsToInput(strings.Split(s, "\n"))
}




// Fitting is the result from the fitting parser
type Fitting struct {
	Items []ListingItem
	lines []int
}

// Name returns the parser name
func (r *Fitting) Name() string {
	return "fitting"
}

// Lines returns the lines that this result is made from
func (r *Fitting) Lines() []int {
	return r.lines
}

var fittingBlacklist = map[string]bool{
	"High power":   true,
	"Medium power": true,
	"Low power":    true,
	"Rig Slot":     true,
	"Sub System":   true,
	"Charges":      true,
	"Drones":       true,
	"Fuel":         true,
}


type Listing struct {
	Items []ListingItem
	lines []int
}

// Name returns the parser name
func (r *Listing) Name() string {
	return "listing"
}

// Lines returns the lines that this result is made from
func (r *Listing) Lines() []int {
	return r.lines
}

// ListingItem is a single item from a listing result
type ListingItem struct {
	Name     string
	Quantity int64
}

var reListing = regexp.MustCompile(`^\s*([\d,'\.]+?) ?(?:x|X)? ([\S ]+)[\s]*$`)
var reListing2 = regexp.MustCompile(`^([\S ]+?):? (?:x|X)? ?([\d,'\.]+)[\s]*$`)
var reListing3 = regexp.MustCompile(`^\s*([\S ]+)[\s]*$`)
var reListing4 = regexp.MustCompile(`^\s*([\d,'\.]+)\t([\S ]+?)[\s]*$`)
var reListingWithAmmo = regexp.MustCompile(`^([\S ]+), ?([a-zA-Z][\S ]+)[\s]*$`)

func ParseListing(input Input) (ParserResult, Input) {
	listing := &Listing{}

	matchesWithAmmo, rest := regexParseLines(reListingWithAmmo, input)
	matches, rest := regexParseLines(reListing, rest)
	matches2, rest := regexParseLines(reListing2, rest)
	matches3, rest := regexParseLines(reListing3, rest)
	matches4, rest := regexParseLines(reListing4, rest)

	listing.lines = append(listing.lines, regexMatchedLines(matches)...)
	listing.lines = append(listing.lines, regexMatchedLines(matches2)...)
	listing.lines = append(listing.lines, regexMatchedLines(matches3)...)
	listing.lines = append(listing.lines, regexMatchedLines(matches4)...)
	listing.lines = append(listing.lines, regexMatchedLines(matchesWithAmmo)...)

	// collect items
	matchgroup := make(map[ListingItem]int64)
	for _, match := range matches {
		matchgroup[ListingItem{Name: CleanTypeName(match[2])}] += ToInt(match[1])
	}

	for _, match := range matches2 {
		matchgroup[ListingItem{Name: CleanTypeName(match[1])}] += ToInt(match[2])
	}

	for _, match := range matches3 {
		matchgroup[ListingItem{Name: CleanTypeName(match[1])}]++
	}

	for _, match := range matches4 {
		matchgroup[ListingItem{Name: CleanTypeName(match[2])}] += ToInt(match[1])
	}

	for _, match := range matchesWithAmmo {
		matchgroup[ListingItem{Name: CleanTypeName(match[1])}]++
		matchgroup[ListingItem{Name: CleanTypeName(match[2])}]++
	}

	// add items w/totals
	for item, quantity := range matchgroup {
		item.Quantity = quantity
		listing.Items = append(listing.Items, item)
	}

	sort.Slice(listing.Items, func(i, j int) bool {
		return fmt.Sprintf("%v", listing.Items[i]) < fmt.Sprintf("%v", listing.Items[j])
	})
	sort.Ints(listing.lines)
	return listing, rest
}

//export ParseFittingTest
func ParseFittingTest(input_string *C.char) (*C.char) {

	input := StringToInput(C.GoString(input_string))

	fitting := &Fitting{}

	// remove blacklisted lines
	isFitting := false
	for i, line := range input {
		_, blacklisted := fittingBlacklist[line]
		if blacklisted {
			isFitting = true
			fitting.lines = append(fitting.lines, i)
			delete(input, i)
		}
	}
	/*if !isFitting {
		return nil
	}*/

	var items string

	result, rest := ParseListing(input)
	listingResult, ok := result.(*Listing)

	fitting.Items = listingResult.Items
	fitting.lines = append(fitting.lines, listingResult.Lines()...)
	for i, item := range fitting.Items {
		items = items + CleanTypeName(item.Name) + " _ " +  strconv.FormatInt(item.Quantity, 10) + "\n"
		_ = i
	}
	/*
	sort.Slice(fitting.Items, func(i, j int) bool {
		return fmt.Sprintf("%v", fitting.Items[i]) < fmt.Sprintf("%v", fitting.Items[j])
	})
	sort.Ints(fitting.lines)
	*/
	//return "done"
	_ = ok
	_ = isFitting
	_ = rest

	return C.CString(items)
}

// ParseFitting parses fittings
func ParseFitting(input Input) (ParserResult, Input) {
	fitting := &Fitting{}

	// remove blacklisted lines
	isFitting := false
	for i, line := range input {
		_, blacklisted := fittingBlacklist[line]
		if blacklisted {
			isFitting = true
			fitting.lines = append(fitting.lines, i)
			delete(input, i)
		}
	}
	if !isFitting {
		return nil, input
	}

	result, rest := ParseListing(input)
	listingResult, ok := result.(*Listing)
	_ = ok
	fitting.Items = listingResult.Items
	fitting.lines = append(fitting.lines, listingResult.Lines()...)

	sort.Slice(fitting.Items, func(i, j int) bool {
		return fmt.Sprintf("%v", fitting.Items[i]) < fmt.Sprintf("%v", fitting.Items[j])
	})
	sort.Ints(fitting.lines)
	return fitting, rest
}

func main() {}
