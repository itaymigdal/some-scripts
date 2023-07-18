
$source = @"
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

public class Screenshot
{
    public static List<Bitmap> CaptureScreens()
    {
        var results = new List<Bitmap>();
        var allScreens = Screen.AllScreens;

        foreach (Screen screen in allScreens)
        {
            try
            {
                Rectangle bounds = screen.Bounds;
                using (Bitmap bitmap = new Bitmap(bounds.Width, bounds.Height))
                {
                    using (Graphics graphics = Graphics.FromImage(bitmap))
                    {
                        graphics.CopyFromScreen(new Point(bounds.Left, bounds.Top), Point.Empty, bounds.Size);
                    }

                    results.Add((Bitmap)bitmap.Clone());
                }
            }
            catch (Exception)
            {
                // Handle any exceptions here
            }
        }

        return results;
    }
}
"@

Add-Type -TypeDefinition $source -ReferencedAssemblies System.Drawing, System.Windows.Forms

$screenshots = [Screenshot]::CaptureScreens()

for ($i = 0; $i -lt $screenshots.Count; $i++){
    $screenshot = $screenshots[$i]
    $screenshot.Save("$env:TEMP/Display ($($i+1)).png")
    $screenshot.Dispose()
}
