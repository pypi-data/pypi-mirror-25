Vespa stands for Versatile Simulation, Pulses, and Analysis. The Vespa
package migrates three previously developed magnetic resonance spectroscopy (MRS) software tools
into an integrated, open source, open development platform. The applications are called Pulse,
Simulation and Analysis and allow users to design RF pulses, create spectral simulations and
perform spectral data processing and analysis.  A (newer) fourth application called Priorset
creates simulated spectroscopy data sets.

The Vespa project addresses previous software limitations, including: non-standard data access,
closed source multiple language software that complicate algorithm extension and comparison,
lack of integration between programs for sharing prior information, and incomplete or missing
documentation and educational content.

These applications can be run separately but can communicate among themselves via a shared
database of objects/results.  One example of inter-application sharing might be that
Simulation would make use of an RF pulse designed in Pulse application to create a more
realistic MR simulation.

