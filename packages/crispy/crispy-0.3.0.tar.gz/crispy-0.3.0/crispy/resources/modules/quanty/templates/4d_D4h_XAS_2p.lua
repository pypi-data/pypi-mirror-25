--------------------------------------------------------------------------------
-- Quanty input file generated using Crispy.
--
-- elements: 4d transition metals
-- symmetry: D4h
-- experiment: XAS
-- edge: L2,3 (2p)
--------------------------------------------------------------------------------
Verbosity(0x00FF)

--------------------------------------------------------------------------------
-- Initialize the Hamiltonians.
--------------------------------------------------------------------------------
H_i = 0
H_f = 0

--------------------------------------------------------------------------------
-- Toggle the Hamiltonian terms.
--------------------------------------------------------------------------------
H_atomic = $H_atomic
H_cf     = $H_cf

--------------------------------------------------------------------------------
-- Define the number of electrons, shells, etc.
--------------------------------------------------------------------------------
NBosons = 0
NFermions = 16

NElectrons_2p = 6
NElectrons_4d = $NElectrons_4d

IndexDn_2p = {0, 2, 4}
IndexUp_2p = {1, 3, 5}
IndexDn_4d = {6, 8, 10, 12, 14}
IndexUp_4d = {7, 9, 11, 13, 15}

--------------------------------------------------------------------------------
-- Define the atomic term.
--------------------------------------------------------------------------------
N_2p = NewOperator('Number', NFermions, IndexUp_2p, IndexUp_2p, {1, 1, 1})
     + NewOperator('Number', NFermions, IndexDn_2p, IndexDn_2p, {1, 1, 1})

N_4d = NewOperator('Number', NFermions, IndexUp_4d, IndexUp_4d, {1, 1, 1, 1, 1})
     + NewOperator('Number', NFermions, IndexDn_4d, IndexDn_4d, {1, 1, 1, 1, 1})

if H_atomic == 1 then
    F0_4d_4d = NewOperator('U', NFermions, IndexUp_4d, IndexDn_4d, {1, 0, 0})
    F2_4d_4d = NewOperator('U', NFermions, IndexUp_4d, IndexDn_4d, {0, 1, 0})
    F4_4d_4d = NewOperator('U', NFermions, IndexUp_4d, IndexDn_4d, {0, 0, 1})

    F0_2p_4d = NewOperator('U', NFermions, IndexUp_2p, IndexDn_2p, IndexUp_4d, IndexDn_4d, {1, 0}, {0, 0})
    F2_2p_4d = NewOperator('U', NFermions, IndexUp_2p, IndexDn_2p, IndexUp_4d, IndexDn_4d, {0, 1}, {0, 0})
    G1_2p_4d = NewOperator('U', NFermions, IndexUp_2p, IndexDn_2p, IndexUp_4d, IndexDn_4d, {0, 0}, {1, 0})
    G3_2p_4d = NewOperator('U', NFermions, IndexUp_2p, IndexDn_2p, IndexUp_4d, IndexDn_4d, {0, 0}, {0, 1})

    U_4d_4d_i  = $U(4d,4d)_i_value * $U(4d,4d)_i_scaling
    F2_4d_4d_i = $F2(4d,4d)_i_value * $F2(4d,4d)_i_scaling
    F4_4d_4d_i = $F4(4d,4d)_i_value * $F4(4d,4d)_i_scaling
    F0_4d_4d_i = U_4d_4d_i + 2 / 63 * F2_4d_4d_i + 2 / 63 * F4_4d_4d_i

    U_4d_4d_f  = $U(4d,4d)_f_value * $U(4d,4d)_f_scaling
    F2_4d_4d_f = $F2(4d,4d)_f_value * $F2(4d,4d)_f_scaling
    F4_4d_4d_f = $F4(4d,4d)_f_value * $F4(4d,4d)_f_scaling
    F0_4d_4d_f = U_4d_4d_f + 2 / 63 * F2_4d_4d_f + 2 / 63 * F4_4d_4d_f
    U_2p_4d_f  = $U(2p,4d)_f_value * $U(2p,4d)_f_scaling
    F2_2p_4d_f = $F2(2p,4d)_f_value * $F2(2p,4d)_f_scaling
    G1_2p_4d_f = $G1(2p,4d)_f_value * $G1(2p,4d)_f_scaling
    G3_2p_4d_f = $G3(2p,4d)_f_value * $G3(2p,4d)_f_scaling
    F0_2p_4d_f = U_2p_4d_f + 1 / 15 * G1_2p_4d_f + 3 / 70 * G3_2p_4d_f

    H_i = H_i
        + F0_4d_4d_i * F0_4d_4d
        + F2_4d_4d_i * F2_4d_4d
        + F4_4d_4d_i * F4_4d_4d

    H_f = H_f
        + F0_4d_4d_f * F0_4d_4d
        + F2_4d_4d_f * F2_4d_4d
        + F4_4d_4d_f * F4_4d_4d
        + F0_2p_4d_f * F0_2p_4d
        + F2_2p_4d_f * F2_2p_4d
        + G1_2p_4d_f * G1_2p_4d
        + G3_2p_4d_f * G3_2p_4d

    ldots_4d = NewOperator('ldots', NFermions, IndexUp_4d, IndexDn_4d)

    ldots_2p = NewOperator('ldots', NFermions, IndexUp_2p, IndexDn_2p)

    zeta_4d_i = $zeta(4d)_i_value * $zeta(4d)_i_scaling

    zeta_4d_f = $zeta(4d)_f_value * $zeta(4d)_f_scaling
    zeta_2p_f = $zeta(2p)_f_value * $zeta(2p)_f_scaling

    H_i = H_i
        + zeta_4d_i * ldots_4d

    H_f = H_f
        + zeta_4d_f * ldots_4d
        + zeta_2p_f * ldots_2p
end

--------------------------------------------------------------------------------
-- Define the crystal field term.
--------------------------------------------------------------------------------
if H_cf == 1 then
    -- PotentialExpandedOnClm('D4h', 2, {Ea1g, Eb1g, Eb2g, Eeg})
    Dq_4d = NewOperator('CF', NFermions, IndexUp_4d, IndexDn_4d, PotentialExpandedOnClm('D4h', 2, { 6,  6, -4, -4}))
    Ds_4d = NewOperator('CF', NFermions, IndexUp_4d, IndexDn_4d, PotentialExpandedOnClm('D4h', 2, {-2,  2,  2, -1}))
    Dt_4d = NewOperator('CF', NFermions, IndexUp_4d, IndexDn_4d, PotentialExpandedOnClm('D4h', 2, {-6, -1, -1,  4}))

    Dq_4d_i = $Dq(4d)_i_value * $Dq(4d)_i_scaling
    Ds_4d_i = $Ds(4d)_i_value * $Ds(4d)_i_scaling
    Dt_4d_i = $Dt(4d)_i_value * $Dt(4d)_i_scaling

    Dq_4d_f = $Dq(4d)_f_value * $Dq(4d)_f_scaling
    Ds_4d_f = $Ds(4d)_f_value * $Ds(4d)_f_scaling
    Dt_4d_f = $Dt(4d)_f_value * $Dt(4d)_f_scaling

    H_i = H_i
        + Dq_4d_i * Dq_4d
        + Ds_4d_i * Ds_4d
        + Dt_4d_i * Dt_4d

    H_f = H_f
        + Dq_4d_f * Dq_4d
        + Ds_4d_f * Ds_4d
        + Dt_4d_f * Dt_4d
end

--------------------------------------------------------------------------------
-- Define the magnetic field term.
--------------------------------------------------------------------------------
Sx_4d    = NewOperator('Sx'   , NFermions, IndexUp_4d, IndexDn_4d)
Sy_4d    = NewOperator('Sy'   , NFermions, IndexUp_4d, IndexDn_4d)
Sz_4d    = NewOperator('Sz'   , NFermions, IndexUp_4d, IndexDn_4d)
Ssqr_4d  = NewOperator('Ssqr' , NFermions, IndexUp_4d, IndexDn_4d)
Splus_4d = NewOperator('Splus', NFermions, IndexUp_4d, IndexDn_4d)
Smin_4d  = NewOperator('Smin' , NFermions, IndexUp_4d, IndexDn_4d)

Lx_4d    = NewOperator('Lx'   , NFermions, IndexUp_4d, IndexDn_4d)
Ly_4d    = NewOperator('Ly'   , NFermions, IndexUp_4d, IndexDn_4d)
Lz_4d    = NewOperator('Lz'   , NFermions, IndexUp_4d, IndexDn_4d)
Lsqr_4d  = NewOperator('Lsqr' , NFermions, IndexUp_4d, IndexDn_4d)
Lplus_4d = NewOperator('Lplus', NFermions, IndexUp_4d, IndexDn_4d)
Lmin_4d  = NewOperator('Lmin' , NFermions, IndexUp_4d, IndexDn_4d)

Jx_4d    = NewOperator('Jx'   , NFermions, IndexUp_4d, IndexDn_4d)
Jy_4d    = NewOperator('Jy'   , NFermions, IndexUp_4d, IndexDn_4d)
Jz_4d    = NewOperator('Jz'   , NFermions, IndexUp_4d, IndexDn_4d)
Jsqr_4d  = NewOperator('Jsqr' , NFermions, IndexUp_4d, IndexDn_4d)
Jplus_4d = NewOperator('Jplus', NFermions, IndexUp_4d, IndexDn_4d)
Jmin_4d  = NewOperator('Jmin' , NFermions, IndexUp_4d, IndexDn_4d)

Sx = Sx_4d
Sy = Sy_4d
Sz = Sz_4d

Lx = Lx_4d
Ly = Ly_4d
Lz = Lz_4d

Jx = Jx_4d
Jy = Jy_4d
Jz = Jz_4d

Ssqr = Sx * Sx + Sy * Sy + Sz * Sz
Lsqr = Lx * Lx + Ly * Ly + Lz * Lz
Jsqr = Jx * Jx + Jy * Jy + Jz * Jz

Bx = $Bx * EnergyUnits.Tesla.value
By = $By * EnergyUnits.Tesla.value
Bz = $Bz * EnergyUnits.Tesla.value

B = Bx * (2 * Sx + Lx)
  + By * (2 * Sy + Ly)
  + Bz * (2 * Sz + Lz)

H_i = H_i
    + B

H_f = H_f
    + B

--------------------------------------------------------------------------------
-- Define the restrictions and set the number of initial states.
--------------------------------------------------------------------------------
InitialRestrictions = {NFermions, NBosons, {'111111 0000000000', NElectrons_2p, NElectrons_2p},
                                           {'000000 1111111111', NElectrons_4d, NElectrons_4d}}

Operators = {H_i, Ssqr, Lsqr, Jsqr, Sz, Lz, Jz, N_2p, N_4d}
header = '\nAnalysis of the initial Hamiltonian:\n'
header = header .. '==============================================================================================\n'
header = header .. '   i       <E>     <S^2>     <L^2>     <J^2>      <Sz>      <Lz>      <Jz>    <N_2p>    <N_4d>\n'
header = header .. '==============================================================================================\n'
footer = '==============================================================================================\n'

-- Define the temperature.
T = $T * EnergyUnits.Kelvin.value

 -- Approximate machine epsilon.
epsilon = 2.22e-16
Z = 0

NPsis = $NPsis
NPsisAuto = $NPsisAuto

if NPsisAuto == 1 and NPsis ~= 1 then
    NPsis = 1
    NPsisIncrement = 8
    NPsisIsConverged = false
    dZ = {}

    while not NPsisIsConverged do
        if CalculationRestrictions == nil then
            Psis = Eigensystem(H_i, InitialRestrictions, NPsis)
        else
            Psis = Eigensystem(H_i, InitialRestrictions, NPsis, {'restrictions', CalculationRestrictions})
        end

        if not (type(Psis) == 'table') then
            Psis = {Psis}
        end

        E_gs = Psis[1] * H_i * Psis[1]

        for i, Psi in ipairs(Psis) do
            E = Psi * H_i * Psi

            if math.abs(E - E_gs) < epsilon then
                dZ[i] = 1
            else
                dZ[i] = math.exp(-(E - E_gs) / T)
            end

            Z = Z + dZ[i]

            if (dZ[i] / Z) < math.sqrt(epsilon) then
                i = i - 1
                NPsisIsConverged = true
                NPsis = i
                Psis = {unpack(Psis, 1, i)}
                dZ = {unpack(dZ, 1, i)}
                break
            end
        end

        if NPsisIsConverged then
            break
        else
            NPsis = NPsis + NPsisIncrement
        end
    end
    Z = 0
else
        if CalculationRestrictions == nil then
            Psis = Eigensystem(H_i, InitialRestrictions, NPsis)
        else
            Psis = Eigensystem(H_i, InitialRestrictions, NPsis, {'restrictions', CalculationRestrictions})
        end

    if not (type(Psis) == 'table') then
        Psis = {Psis}
    end
end

io.write(header)
for i, Psi in ipairs(Psis) do
    io.write(string.format('%4d', i))
    for j, Operator in ipairs(Operators) do
        io.write(string.format('%10.4f', Complex.Re(Psi * Operator * Psi)))
    end
    io.write('\n')
end
io.write(footer)

--------------------------------------------------------------------------------
-- Define the transition operators.
--------------------------------------------------------------------------------
t = math.sqrt(1/2);

Tiso_2p_4d = NewOperator('CF', NFermions, IndexUp_4d, IndexDn_4d, IndexUp_2p, IndexDn_2p, {{1, -1, t    }, {1, 1, -t    }}) -- Tx
           + NewOperator('CF', NFermions, IndexUp_4d, IndexDn_4d, IndexUp_2p, IndexDn_2p, {{1, -1, t * I}, {1, 1,  t * I}}) -- Ty
           + NewOperator('CF', NFermions, IndexUp_4d, IndexDn_4d, IndexUp_2p, IndexDn_2p, {{1,  0, 1    }                }) -- Tz

--------------------------------------------------------------------------------
-- Calculate and save the spectra.
--------------------------------------------------------------------------------
Giso = 0

Emin = $Emin1
Emax = $Emax1
Gamma = $Gamma1
NE = $NE1

E_gs = Psis[1] * H_i * Psis[1]

for i, Psi in ipairs(Psis) do
    E = Psi * H_i * Psi

    if math.abs(E - E_gs) < epsilon then
        dZ = 1
    else
        dZ = math.exp(-(E - E_gs) / T)
    end

    if (dZ < math.sqrt(epsilon)) then
        break
    end

    Z = Z + dZ

    Giso = Giso + CreateSpectra(H_f, Tiso_2p_4d, Psi, {{'Emin', Emin}, {'Emax', Emax}, {'NE', NE}, {'Gamma', Gamma}}) * dZ
end

Giso = Giso / Z
Giso.Print({{'file', '$baseName' .. '_iso.spec'}})

