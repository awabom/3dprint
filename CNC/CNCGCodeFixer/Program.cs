using System.Globalization;
using System.Text.RegularExpressions;

namespace CNC
{
    public class Program
    {
        static void Main(string[] args)
        {
            string fileName = args[0];
            var gcode = File.ReadAllLines(fileName).ToList();
            var result = CNCGCode.Fix(gcode);
            File.WriteAllText(fileName, string.Join(Environment.NewLine, result));
        }
    }

    public class CNCGCode
    {
        const decimal SafeZ = 2.0m;
        const string GcodeHopToSafety = "G1 Z2 F600 ; CNC Z-HOP";

        const StringComparison Ord = StringComparison.Ordinal;
        static readonly CultureInfo IC = CultureInfo.InvariantCulture;

        static readonly Regex reMoveCommand = new("^G[0123] .*");
        static readonly Regex reMoveZ = new("^G[01] .*Z(?<z>[^ ;]+).*");
        static readonly Regex reMoveF = new("^G[01] .*F(?<f>[^ ;]+).*");

        public static List<string> Fix(List<string> gcode)
        {
            List<string> result = new List<string>();
            decimal currentZ = SafeZ - 1m; // make the currentZ unsafe
            string? latestZCommand = null; // the latest z-move made in original g-code
            decimal? latestZ = null;
            string? restoreFeedrateCommand = null; // command to restore latest feedrate set in original g-code

            // Z-HOP on TRAVEL MOVE
            foreach (var line in gcode)
            {
                // Check for current feed-rate settings
                var moveF = reMoveF.Match(line);
                bool restoreSkipLine;
                if (moveF.Success)
                {
                    restoreFeedrateCommand = "G1 F" + moveF.Groups["f"].Value + " ; CNC RESTORE FEEDRATE";
                    restoreSkipLine = true;
                }
                else
                {
                    restoreSkipLine = false;
                }

                // Check for z-moves
                var moveZ = reMoveZ.Match(line);
                if (moveZ.Success)
                {
                    latestZCommand = line;
                    latestZ = decimal.Parse(moveZ.Groups["z"].Value, IC);
                    currentZ = latestZ.Value;
                }
                else // not a z-move, check for travel/extrude
                {
                    var isMove = reMoveCommand.IsMatch(line);
                    var isExtrude = line.Contains(" E", Ord);

                    if (isMove)
                    {
                        // Travel - A move without extrude
                        if (!isExtrude)
                        {
                            if (currentZ < SafeZ)
                            {
                                result.Add(GcodeHopToSafety);
                                if (restoreFeedrateCommand != null && !restoreSkipLine)
                                    result.Add(restoreFeedrateCommand);
                                currentZ = SafeZ;
                            }
                        }
                        else
                        { // is extrude
                            if (latestZ == null || latestZCommand == null)
                                throw new NullReferenceException();

                            if (currentZ != latestZ.Value)
                            {
                                result.Add(latestZCommand + "; CNC Z-UNHOP");
                                if (restoreFeedrateCommand != null && !restoreSkipLine)
                                    result.Add(restoreFeedrateCommand);
                                currentZ = latestZ.Value;
                            }
                        }

                    }
                }

                result.Add(line);
            }

            // DISABLE PrusaSlicer's first Z move
            for (int i=0; i < result.Count; i++)
            {
                var zMatch = reMoveZ.Match(result[i]);
                if (zMatch.Success && decimal.Parse(zMatch.Groups["z"].Value) < 0)
                {
                    result[i] = "; CNC REMOVED FIRST CUTTING Z-MOVE: " + result[i];
                    break;
                }
            }

            return result;
        }
    }

}